"""
Flask web server for the MIPS Pipeline Simulator UI.

Run with:
    cd web
    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000 in your browser.
"""

import sys
import os
import io
import tempfile
import contextlib

# Allow importing MIPSSimulator from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from MIPSSimulator.Decoder import Decoder
from MIPSSimulator.Pipeline import Pipeline
from MIPSSimulator.Instruction import R_TYPE_FUNCTS, I_TYPE_OPCODES, J_TYPE_OPCODES

app = Flask(__name__)

REGISTER_NAMES = [
    "zero", "at", "v0", "v1",
    "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3",
    "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3",
    "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1",
    "gp", "sp", "fp", "ra",
]


def _format_binary_fields(instr) -> str:
    b = instr.binary
    if instr.opcode in R_TYPE_FUNCTS or instr.opcode == "NOP":
        return (f"opcode={b[0:6]} | rs={b[6:11]} | rt={b[11:16]}"
                f" | rd={b[16:21]} | shamt={b[21:26]} | funct={b[26:32]}")
    if instr.opcode in I_TYPE_OPCODES:
        return f"opcode={b[0:6]} | rs={b[6:11]} | rt={b[11:16]} | imm={b[16:32]}"
    if instr.opcode in J_TYPE_OPCODES:
        return f"opcode={b[0:6]} | target={b[6:32]}"
    return b


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run", methods=["POST"])
def run_simulation():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    code = data.get("code", "").strip()
    debug = data.get("debug", False)
    show_hex = data.get("hex", False)
    show_binary = data.get("binary", False)

    if not code:
        return jsonify({"success": False, "error": "No assembly code provided"}), 400

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".asm", delete=False) as f:
            f.write(code)
            tmp_path = f.name

        stdout_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture):
            decoder = Decoder(tmp_path)
            instructions = decoder.decode()

            if show_hex:
                print("\n===== Hex Representation =====")
                for instr in instructions:
                    hex_val = f"0x{int(instr.binary, 2):08x}"
                    print(f"  {instr.address:02}: {hex_val}  [{instr.source}]")

            if show_binary:
                print("\n===== Binary Representation =====")
                for instr in instructions:
                    print(f"  {instr.address:02}: [{instr.source}]")
                    print(f"      {_format_binary_fields(instr)}")

            pipeline = Pipeline(instructions)
            pipeline.run(debug=debug)

        # RegisterFile.dump() returns a list[int] of length 32
        regs_raw = pipeline.register_file.dump()
        registers = [
            {"index": i, "name": REGISTER_NAMES[i], "value": regs_raw[i]}
            for i in range(32)
        ]

        # Memory.dump() returns dict[int, int] of non-zero entries only
        mem_raw = pipeline.memory.dump()
        memory = [
            {"address": addr, "value": val}
            for addr, val in mem_raw.items()
        ]

        return jsonify({
            "success": True,
            "output": stdout_capture.getvalue(),
            "registers": registers,
            "memory": memory,
        })

    except KeyError as e:
        return jsonify({"success": False, "error": f"Undefined label: {e.args[0]}"})
    except (ValueError, IndexError, SyntaxError) as e:
        return jsonify({"success": False, "error": str(e)})
    except Exception:
        return jsonify({"success": False, "error": "An unexpected error occurred while running the simulation."})

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
