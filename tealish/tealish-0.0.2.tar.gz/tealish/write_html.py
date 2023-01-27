import sys
from tealish import TealishCompiler


def html_formatter(node, output):
    if hasattr(node, "html"):
        output = node.html(output)
    return output


def cli():
    filename = sys.argv[1]
    compiler = TealishCompiler(open(filename).readlines())
    compiler.compile()
    output = compiler.reformat(html_formatter)

    output = (
        """
    <html>
    <head>
    <style>
    .TxnField {
        background-color: #EFE;
    }
    .Variable {
        background-color: #FEE;
    }
    body {
        font-family: mono;
    }
    #sidebar {
        width: 400px;
        border: 1px solid #ccc;
        position: fixed;
        top: 10px;
        right: 10px;
        padding: 10px;
        background-color: #eeec;
    }
    </style>
    <script src="../test.trace.js"></script>
    </head>
    <body>
    <pre id="sidebar">
    </pre>
    <pre>
    """
        + output
        + """
    </pre>
    <script>
    var step = 0;
    var currentSlots = {};

    function next(){
        step += 1;
        var s = trace.steps[step];
        var span = document.querySelector(`.line[data-line="${s.line_no + 1}"]`)
        span.style.backgroundColor = "#AFA";
        span.querySelectorAll(".Variable[data-slot]").forEach(function(x){
            console.log(x.dataset.name, x.dataset.slot, tealValue(s.prev_scratch[x.dataset.slot]));
        })
        span.querySelectorAll(".assignment[data-slot]").forEach(function(x){
            console.log(x.dataset.name, x.dataset.slot, tealValue(s.scratch[x.dataset.slot]));
            currentSlots[x.dataset.name] = tealValue(s.scratch[x.dataset.slot]);
            updateSlots(currentSlots);
        })
        span.scrollIntoView({behavior: "smooth", block: "center"});

    }

    function updateSlots(data){
        var s = Object.keys(currentSlots).map(k => `${k}: ${currentSlots[k]}`).join("\\n")
        sidebar.innerHTML = s;
    }

    function tealValue(value){
        if(value){
            return value.tt == 2 ? value.ui || 0: value.tb;
        }
    }

    function lookupTealLine(teal_line){
        var i = trace.history.findIndex(function(t){return trace.pc_map[t.pc] == teal_line});
        var stack = trace.history[i + 1].stack;
        var value = stack[stack.length - 1];
        return tealValue(value);
    }

    function lookupStackValueForElement(e){
        var value = lookupTealLine(parseInt(e.dataset.tealLine) - 1);
        updateSlots(currentSlots)
        sidebar.innerHTML += "\\n\\n" + e.innerText + ": " + value;
    }

    function lookupSlotValueForElement(e){
        var slot = parseInt(e.dataset.slot);
        var line = parseInt(e.parentElement.dataset.line);
        var slots = trace.steps.find(s => s.line_no == (line - 1)).scratch;
        var value = tealValue(slots[slot]);
        updateSlots(currentSlots);
        sidebar.innerHTML += "\\n\\n" + e.innerText + ": " + value;
    }

    document.querySelectorAll("[data-teal-line]").forEach(function(e){
        e.onclick = function(event){
            event.stopPropagation();
            lookupStackValueForElement(event.target);
        }
    })

    document.querySelectorAll(".assignment[data-slot]").forEach(function(e){
        e.onclick = function(event){
            event.stopPropagation();
            lookupSlotValueForElement(event.target);
        }
    })
    document.onkeyup = function(e){if(e.key == "n"){next()}};
    </script>
    </body>
    </html>
    """
    )

    if len(sys.argv) == 2:
        output_filename = filename
    else:
        output_filename = sys.argv[2]

    if output_filename == "-":
        print(output)
    else:
        with open(output_filename, "w") as f:
            f.write(output)


if __name__ == "__main__":
    cli()
