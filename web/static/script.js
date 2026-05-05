const DEFAULT_CODE = `# TestArithmetic.asm
# Tests arithmetic and logical instructions.
# NOPs are inserted to avoid data hazards.
#
# Expected results:
#   $t0=12  $t1=10  $t2=3
#   $t3=22  $t4=2   $t5=36
#   $t6=8   $t7=14  $s0=27

        ADDI $t0, $zero, 12
        ADDI $t1, $zero, 10
        ADDI $t2, $zero, 3
        NOP
        NOP
        ADD  $t3, $t0, $t1
        SUB  $t4, $t0, $t1
        MUL  $t5, $t0, $t2
        AND  $t6, $t0, $t1
        OR   $t7, $t0, $t1
        ADDI $s0, $t3, 5
        NOP
`;

// ── DOM refs ──────────────────────────────────────────────
const editor       = document.getElementById("code-editor");
const lineNumbers  = document.getElementById("line-numbers");
const runBtn       = document.getElementById("run-btn");
const runBtnIcon   = document.getElementById("run-icon");
const outputTerm   = document.getElementById("output-terminal");
const regsGrid     = document.getElementById("registers-grid");
const memContent   = document.getElementById("memory-content");
const errorBanner  = document.getElementById("error-banner");
const tabRegs      = document.getElementById("tab-registers-btn");
const tabMem       = document.getElementById("tab-memory-btn");
const regCount     = document.getElementById("reg-count");
const memCount     = document.getElementById("mem-count");

// ── Editor setup ──────────────────────────────────────────
editor.value = DEFAULT_CODE;
updateLineNumbers();

function updateLineNumbers() {
    const count = editor.value.split("\n").length;
    lineNumbers.textContent = Array.from({ length: count }, (_, i) => i + 1).join("\n");
}

editor.addEventListener("input", updateLineNumbers);
editor.addEventListener("scroll", () => { lineNumbers.scrollTop = editor.scrollTop; });

// Tab key inserts spaces instead of changing focus
editor.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
        e.preventDefault();
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.slice(0, start) + "        " + editor.value.slice(end);
        editor.selectionStart = editor.selectionEnd = start + 8;
        updateLineNumbers();
    }
});

// ── Tabs ──────────────────────────────────────────────────
document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => activateTab(btn.dataset.tab));
});

function activateTab(name) {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(c => c.classList.add("hidden"));
    document.querySelector(`[data-tab="${name}"]`).classList.add("active");
    document.getElementById(`tab-${name}`).classList.remove("hidden");
}

// ── Run ───────────────────────────────────────────────────
runBtn.addEventListener("click", runSimulation);

document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        runSimulation();
    }
});

async function runSimulation() {
    const code = editor.value.trim();
    if (!code || runBtn.disabled) return;

    setLoading(true);
    hideError();

    try {
        const res = await fetch("/api/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code,
                debug:  document.getElementById("opt-debug").checked,
                hex:    document.getElementById("opt-hex").checked,
                binary: document.getElementById("opt-binary").checked,
            }),
        });

        const data = await res.json();

        if (data.success) {
            outputTerm.textContent = data.output || "";
            outputTerm.classList.remove("error");
            renderRegisters(data.registers);
            renderMemory(data.memory);
            activateTab("output");
        } else {
            showError(data.error);
            outputTerm.textContent = `Error: ${data.error}`;
            outputTerm.classList.add("error");
            activateTab("output");
        }
    } catch (err) {
        showError(`Network error: ${err.message}`);
        outputTerm.textContent = `Network error: ${err.message}`;
        outputTerm.classList.add("error");
        activateTab("output");
    } finally {
        setLoading(false);
    }
}

function setLoading(on) {
    runBtn.disabled = on;
    runBtn.classList.toggle("loading", on);
}

function showError(msg) {
    errorBanner.textContent = msg;
    errorBanner.classList.add("visible");
}

function hideError() {
    errorBanner.classList.remove("visible");
}

// ── Render registers ──────────────────────────────────────
function renderRegisters(registers) {
    if (!registers?.length) {
        regsGrid.innerHTML = '<p class="placeholder">No register data.</p>';
        regCount.textContent = "—";
        return;
    }

    const nonzero = registers.filter(r => r.value !== 0 && r.index !== 0);
    regCount.textContent = nonzero.length;

    regsGrid.innerHTML = registers.map(reg => {
        const nz = reg.value !== 0;
        return `
        <div class="reg-card ${nz ? "nonzero" : ""}">
            <div class="reg-name">
                <span class="reg-alias">$${reg.name}</span>
                <span>&nbsp;($${reg.index})</span>
            </div>
            <div class="reg-value">${reg.value}</div>
        </div>`;
    }).join("");
}

// ── Render memory ─────────────────────────────────────────
function renderMemory(memory) {
    memCount.textContent = memory?.length ?? "—";

    if (!memory?.length) {
        memContent.innerHTML = '<p class="memory-empty">No memory writes in this program.</p>';
        return;
    }

    const rows = memory.map(entry => {
        const addrHex = "0x" + entry.address.toString(16).padStart(8, "0").toUpperCase();
        const valHex  = "0x" + (entry.value >>> 0).toString(16).padStart(8, "0").toUpperCase();
        return `<tr>
            <td class="cell-addr">${entry.address}</td>
            <td class="cell-addr-hex">${addrHex}</td>
            <td class="cell-val">${entry.value}</td>
            <td class="cell-val-hex">${valHex}</td>
        </tr>`;
    }).join("");

    memContent.innerHTML = `
        <table class="memory-table">
            <thead><tr>
                <th>Address</th>
                <th>Address (hex)</th>
                <th>Value</th>
                <th>Value (hex)</th>
            </tr></thead>
            <tbody>${rows}</tbody>
        </table>`;
}
