def get_session_id() -> str:
    # Working on streamlit==1.17.0
    from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
    ctx = get_script_run_ctx()
    if ctx is None:
        raise Exception("Failed to get the thread context")
    return ctx.session_id