

style = """
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

    .QWidget{
        background-color:#CFD8DC;
    }

    QPushButton{
        background-color:#607D8B;
        color: #FFFFFF;
    }

    QPushButton:hover{
        background-color:#455A64;
    }

    QPushButton:!hover{
        background-color:#607D8B;
    }

    QPushButton:disabled{
        background-color:#BDBDBD;
    }

    QComboBox{
        background-color:#FFFFFF;
        color:#212121;
    }

    QDockWidget:title{
        text-align:right;
        color:#212121;
    }

    QAbstractScrollArea{
        background-color:white;
    }

    QLCDNumber{
        background-color:white;
    }
    """
