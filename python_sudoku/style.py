from pathlib import Path

down_arrow = str(Path(__file__).parent.parent / "resources" / "down_arrow.png")
down_arrow = down_arrow.replace("\\", "/")

style = f"""
    /*
    Color Variables for Reference
    -------------------------------------------------------------
    Dark Primary Color = #455A64
    Light Primary Color = #CFD8DC
    Primary Color = #607D8B
    Text/Icons = #FFFFFF
    Accent Color = #03A9F4
    Primary Text = #212121
    Secondary Text = #757575
    Divider Color = #BDBDBD
    */

    .QWidget{{
        background-color:#CFD8DC;
    }}

    QPushButton{{
        background-color:#607D8B;
        color: #FFFFFF;
    }}

    QPushButton:hover{{
        background-color:#455A64;
    }}

    QPushButton:disabled{{
        background-color:#BDBDBD;
    }}

    QToolButton{{
        background-color:#607D8B;
        color: #FFFFFF;
        font-size:10px;
    }}

    QToolButton:hover{{
        background-color:#455A64;
    }}

    QToolButton:disabled{{
        background-color:#BDBDBD;
    }}

    QComboBox{{
        background-color:#FFFFFF;
        color:#212121;
    }}

    QComboBox:drop-down{{
        background-color:#607D8B;
    }}

    QComboBox:drop-down:hover{{
        background-color:#455A64;
    }}

    QComboBox::down-arrow {{
        image:url("{down_arrow}");
        width:14px;
        height:14px;
    }}

    QDockWidget:title{{
        text-align:center;
        color:#212121;
    }}

    QAbstractScrollArea{{
        background-color:white;
    }}

    QLCDNumber{{
        background-color:white;
    }}

    QCheckBox {{
        font-size:10px;
    }}
    """
