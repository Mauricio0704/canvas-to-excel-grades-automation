import streamlit as st
import sys
import io
import traceback

# Import functions from the automate_grades package
# The Streamlit app will use these to trigger the grade-writing flows.
# We import lazily inside handlers to avoid running heavy setup on import.
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]

# Ensure the `automate_grades` package directory is on sys.path so sibling modules
# (like write_grades_logic.py and set_up.py) can be imported regardless of where
# this app file lives. Search the parent chain for a folder named 'automate_grades'.
automate_dir = None
for p in Path(__file__).resolve().parents:
    if p.name == "automate_grades":
        automate_dir = str(p)
        break
if automate_dir and automate_dir not in sys.path:
    sys.path.insert(0, automate_dir)

st.set_page_config(page_title="Canvas -> Google Sheets Grades", layout="centered")

st.title("Actualizar Base de Datos de Calificaciones")
st.caption("Herramienta de Prepanet para escribir calificaciones de Canvas a Google Sheets.")

# Helper to capture stdout/stderr and display results
class OutputCapture:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self.buffer = io.StringIO()
        sys.stdout = self.buffer
        sys.stderr = self.buffer
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type:
            traceback.print_exception(exc_type, exc_value, tb)
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def get(self):
        return self.buffer.getvalue()


def safe_import(module_name):
    try:
        return importlib.import_module(module_name)
    except Exception as e:
        st.error(f"Failed to import {module_name}: {e}")
        return None


# Load the write_grades_logic module
write_logic = safe_import("write_grades_logic")
set_up = safe_import("set_up")

# Sidebar controls
with st.form("controls"):
    st.write("Parámetros de actualización")
    course_id = st.text_input("ID Curso (o 'all')", value="")
    assignment_id = st.text_input("ID Semana (o 'all')", value="")
    run_setup = st.checkbox("Ejecutar la inicialización de la hoja de datos (inicio de periodo)")
    submit = st.form_submit_button("Ejecutar")

if submit:
    if run_setup:
        if set_up is None or not hasattr(set_up, "set_up_sheet"):
            st.error("set_up.set_up_sheet not available. Check imports.")
        else:
            st.info("Running sheet setup...")
            with st.spinner("Running set_up_sheet..."):
                with OutputCapture() as out:
                    try:
                        set_up.set_up_sheet()
                    except Exception:
                        traceback.print_exc()
                st.code(out.get())
            st.success("Setup finished.")
    else:
        if write_logic is None:
            st.error("write_grades_logic module not available. Check imports.")
        else:
            # Determine which function to call based on inputs
            # Mirror the CLI logic in automate_grades/main.py
            if (not course_id) or (not assignment_id):
                st.error("ID Curso y ID Semana son necesarios al menos que escoga inicializar la hoja de datos.")
            else:
                try:
                    if assignment_id == "all" and course_id == "all":
                        func = getattr(write_logic, "write_grades_of_all_assignments_of_all_courses", None)
                    elif assignment_id == "all":
                        func = getattr(write_logic, "write_grades_of_all_assignments_of_course", None)
                    elif course_id == "all":
                        func = getattr(write_logic, "write_grades_of_assignment_of_all_courses", None)
                    else:
                        func = getattr(write_logic, "write_grades_of_assignment_of_course", None)

                    if func is None:
                        st.error("Requested function not found in write_grades_logic module.")
                    else:
                        st.info(f"LLamando: {func.__name__}")
                        with st.spinner("Ejecución en curso..."):
                            with OutputCapture() as out:
                                try:
                                    if func.__name__ == "write_grades_of_all_assignments_of_all_courses":
                                        func()
                                    elif func.__name__ == "write_grades_of_all_assignments_of_course":
                                        func(course_id)
                                    elif func.__name__ == "write_grades_of_assignment_of_all_courses":
                                        func(int(assignment_id))
                                    else:
                                        func(course_id, int(assignment_id))
                                except Exception:
                                    traceback.print_exc()
                            st.code(out.get())
                        st.success("Operación Finalizada.")
                except ValueError:
                    st.error("Assignment ID must be an integer when not 'all'.")


st.markdown("---")
st.markdown("If you need help, open the terminal and run the original CLI in `automate_grades/main.py`.")
