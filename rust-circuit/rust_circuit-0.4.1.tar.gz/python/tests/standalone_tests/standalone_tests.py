import rust_circuit as rc

a = rc.Scalar(1)
b = rc.Array.randn(10)
import rust_circuit.algebric_rewrite as ar
import rust_circuit.ui.ui as ui

ui.circuit_graph_ui(b)
import rust_circuit.ui.circuits_very_named_tensor as cvnt
import rust_circuit.ui.very_named_tensor as vnt
