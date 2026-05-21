import os
import sys
import time
import subprocess
import vdf

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QFrame
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class SteamManager(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Steam Library Injector"
        )

        self.resize(
            1100,
            650
        )

        self.paths=[

            os.path.expanduser(
                "~/.local/share/Steam/userdata"
            ),

            os.path.expanduser(
                "~/.steam/steam/userdata"
            )
        ]

        self.steam_userdata=next(

            (
                p for p in self.paths
                if os.path.exists(p)
            ),

            None
        )

        self.setup_ui()

        self.apply_styles()

        self.load_games()

    def setup_ui(self):

        main=QHBoxLayout(self)

        main.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main.setSpacing(
            20
        )

        # ESQUERDA

        left=QFrame()

        left.setObjectName(
            "Panel"
        )

        left_layout=QVBoxLayout(
            left
        )

        title=QLabel(
            "Injetar Novo Atalho"
        )

        title.setObjectName(
            "Title"
        )

        left_layout.addWidget(
            title
        )

        left_layout.addWidget(
            QLabel(
                "Nome:"
            )
        )

        self.nome=QLineEdit()

        self.nome.setPlaceholderText(
            "Ex: Cyberpunk 2077"
        )

        left_layout.addWidget(
            self.nome
        )

        # executável

        left_layout.addWidget(
            QLabel(
                "Executável:"
            )
        )

        exe_layout=QHBoxLayout()

        self.exe=QLineEdit()

        exe_btn=QPushButton(
            "Selecionar"
        )

        exe_btn.clicked.connect(
            self.select_exe
        )

        exe_layout.addWidget(
            self.exe
        )

        exe_layout.addWidget(
            exe_btn
        )

        left_layout.addLayout(
            exe_layout
        )

        # ícone

        left_layout.addWidget(
            QLabel(
                "Ícone:"
            )
        )

        icon_layout=QHBoxLayout()

        self.icon=QLineEdit()

        self.icon.setPlaceholderText(
            "Opcional"
        )

        icon_btn=QPushButton(
            "Selecionar"
        )

        icon_btn.clicked.connect(
            self.select_icon
        )

        icon_layout.addWidget(
            self.icon
        )

        icon_layout.addWidget(
            icon_btn
        )

        left_layout.addLayout(
            icon_layout
        )

        # argumentos

        left_layout.addWidget(
            QLabel(
                "Argumentos:"
            )
        )

        self.args=QLineEdit()

        self.args.setPlaceholderText(
            "MANGOHUD=1 %command%"
        )

        left_layout.addWidget(
            self.args
        )

        preset=QPushButton(
            "Preset Online"
        )

        preset.clicked.connect(
            self.online_preset
        )

        left_layout.addWidget(
            preset
        )

        left_layout.addStretch()

        add=QPushButton(
            "Adicionar à Steam"
        )

        add.setObjectName(
            "AddBtn"
        )

        add.clicked.connect(
            self.add_game
        )

        left_layout.addWidget(
            add
        )

        # DIREITA

        right=QFrame()

        right.setObjectName(
            "Panel"
        )

        right_layout=QVBoxLayout(
            right
        )

        title2=QLabel(
            "Biblioteca Atual"
        )

        title2.setObjectName(
            "Title"
        )

        right_layout.addWidget(
            title2
        )

        self.lista=QListWidget()

        right_layout.addWidget(
            self.lista
        )

        remove=QPushButton(
            "Remover"

        )

        remove.setObjectName(
            "RemoveBtn"
        )

        remove.clicked.connect(
            self.remove_game
        )

        right_layout.addWidget(
            remove
        )

        main.addWidget(
            left,
            4
        )

        main.addWidget(
            right,
            3
        )

    def apply_styles(self):

        self.setStyleSheet("""

QWidget{

background:#171a21;
color:white;
font-size:13px;

}

QFrame#Panel{

background:#1b2838;
border-radius:10px;
border:1px solid #2a475e;

}

QLineEdit{

background:#101822;
padding:8px;
border-radius:5px;
border:1px solid #2a475e;

}

QPushButton{

background:#2a475e;
padding:10px;
border-radius:5px;

}

QPushButton:hover{

background:#3b6283;

}

QPushButton#AddBtn{

background:#8b0000;
border:1px solid #c41e3a;

}

QPushButton#AddBtn:hover{

background:#a50f2d;

}

QPushButton#RemoveBtn{

background:#252020;

}

QLabel#Title{

font-size:20px;
font-weight:bold;

}

QListWidget{

background:#101822;
border-radius:5px;

}

""")

    def select_exe(self):

        arquivo,_=QFileDialog.getOpenFileName(
            self,
            "Executável"
        )

        if arquivo:

            self.exe.setText(
                arquivo
            )

    def select_icon(self):

        arquivo,_=QFileDialog.getOpenFileName(

            self,

            "Ícone",

            "",

            "Imagens (*.png *.jpg *.jpeg *.ico)"
        )

        if arquivo:

            self.icon.setText(
                arquivo
            )

    def online_preset(self):

        self.args.setText(
            'WINEDLLOVERRIDES="OnlineFix64=n;SteamOverlay64=n;winmm=n,b;dnet=n;steam_api64=n;winhttp=n,b" %command%'
        )

    def get_shortcuts(self):

        for user in os.listdir(
            self.steam_userdata
        ):

            path=os.path.join(

                self.steam_userdata,
                user,
                "config",
                "shortcuts.vdf"
            )

            if os.path.exists(
                path
            ):
                return path

    def load_games(self):

        self.lista.clear()

        caminho=self.get_shortcuts()

        if not caminho:
            return

        with open(
            caminho,
            "rb"
        ) as f:

            data=vdf.binary_load(
                f
            )

        for sid,jogo in data.get(
            "shortcuts",
            {}
        ).items():

            nome=jogo.get(
                "AppName",
                "Sem Nome"
            )

            icon=jogo.get(
                "icon",
                ""
            )

            item=QListWidgetItem(
                nome
            )

            item.setData(
                Qt.UserRole,
                sid
            )

            if icon and os.path.exists(icon):

                item.setIcon(
                    QIcon(icon)
                )

            self.lista.addItem(
                item
            )

    def add_game(self):

        nome=self.nome.text().strip()

        exe=self.exe.text().strip()

        args=self.args.text().strip()

        icon=self.icon.text().strip()

        if not nome or not exe:

            QMessageBox.warning(
                self,
                "Erro",
                "Preencha os campos"
            )

            return

        caminho=self.get_shortcuts()

        with open(
            caminho,
            "rb"
        ) as f:

            data=vdf.binary_load(
                f
            )

        for _,jogo in data.get(
            "shortcuts",
            {}
        ).items():

            if jogo.get(
                "AppName"
            )==nome:

                QMessageBox.warning(
                    self,
                    "Duplicado",
                    "Jogo já existe"
                )

                return

        self.close_steam()

        novo=str(
            len(
                data["shortcuts"]
            )
        )

        data["shortcuts"][novo]={

            "appid":0,
            "AppName":nome,
            "Exe":f'"{exe}"',
            "StartDir":f'"{os.path.dirname(exe)}"',
            "LaunchOptions":args,
            "icon":icon,
            "tags":{}
        }

        with open(
            caminho,
            "wb"
        ) as f:

            vdf.binary_dump(
                data,
                f
            )

        self.open_steam()

        self.load_games()

    def remove_game(self):

        item=self.lista.currentItem()

        if not item:
            return

        sid=item.data(
            Qt.UserRole
        )

        caminho=self.get_shortcuts()

        with open(
            caminho,
            "rb"
        ) as f:

            data=vdf.binary_load(
                f
            )

        del data[
            "shortcuts"
        ][sid]

        with open(
            caminho,
            "wb"
        ) as f:

            vdf.binary_dump(
                data,
                f
            )

        self.open_steam()

        self.load_games()

    def close_steam(self):

        subprocess.run(
            [
                "steam",
                "-shutdown"
            ]
        )

        time.sleep(
            2
        )

    def open_steam(self):

        subprocess.Popen(
            ["steam"]
        )


app=QApplication(
    sys.argv
)

janela=SteamManager()

janela.show()

sys.exit(
    app.exec()
)