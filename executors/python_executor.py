import adsk.core, adsk.fusion, traceback
import os


def execute_python_code(code):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # If the environment variable FUSION360_DEBUG is set, start debugpy listener
        if os.environ.get('FUSION360_DEBUG') == '1':
            try:
                import debugpy
                if not debugpy.is_client_connected():
                    debugpy.listen(("127.0.0.1", 9000))
                    ui.messageBox("Waiting for debugger to attach on port 9000...")
                    debugpy.wait_for_client()
            except ImportError:
                ui.messageBox("debugpy module not found, continuing without debugger.")
        
        # Ensure there is an active document, or create one
        if app.documents.count == 0:
            doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        else:
            doc = app.activeDocument
        
        design = app.activeProduct
        rootComp = design.rootComponent
        
        # Prepare the execution environment
        exec_env = {
            'app': app,
            'ui': ui,
            'doc': doc,
            'design': design,
            'rootComp': rootComp,
            'adsk': adsk
        }
        
        # Execute the user provided Python code
        exec(code, exec_env)
    except:
        if 'ui' in locals() and ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
