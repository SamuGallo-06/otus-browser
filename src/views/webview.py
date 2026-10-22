from PySide6.QtCore import Qt, QUrl, QUrlQuery, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineContextMenuRequest

W = QWebEnginePage.WebAction

# Parametri di tracciamento rimossi da "Copy link without trackers".
# Qualsiasi parametro che inizia con "utm_" viene rimosso a prescindere.
TRACKING_PARAMS = {
    "fbclid", "gclid", "dclid", "msclkid", "yclid", "igshid",
    "mc_cid", "mc_eid", "_hsenc", "_hsmi",
}


def clean_url(url: QUrl) -> QUrl:
    """Restituisce una copia dell'URL senza i parametri di tracciamento più comuni."""
    query = QUrlQuery(url)
    removed = False
    for key, _value in query.queryItems():
        if key.lower().startswith("utm_") or key.lower() in TRACKING_PARAMS:
            query.removeAllQueryItems(key)
            removed = True
    if not removed:
        return url
    cleaned = QUrl(url)
    if query.isEmpty():
        cleaned.setQuery("")         # nessun parametro rimasto: niente "?" finale
    else:
        cleaned.setQuery(query)
    return cleaned


class OtusWebView(QWebEngineView):
    # Segnali verso la main window: la view sa *cosa* è stato cliccato,
    # la main window decide *come* aprire schede, finestre, ricerche.
    linkNewTabRequested = Signal(QUrl)
    linkNewWindowRequested = Signal(QUrl)
    searchRequested = Signal(str)
    savePageRequested = Signal()

    # ------------------------------------------------------------------
    # Menu contestuale
    # ------------------------------------------------------------------
    def contextMenuEvent(self, event):
        data = self.lastContextMenuRequest()
        if data is None:
            super().contextMenuEvent(event)
            return

        # Copio subito ciò che serve: i dati descrivono l'ULTIMO clic destro
        link = QUrl(data.linkUrl())
        media = QUrl(data.mediaUrl())
        is_image = (data.mediaType()
                    == QWebEngineContextMenuRequest.MediaType.MediaTypeImage)
        selected = data.selectedText().strip()
        editable = data.isContentEditable()

        menu = QMenu(self)
        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        if link.isValid():
            self._separator(menu)
            self._addLinkActions(menu, link)

        if is_image and media.isValid():
            self._separator(menu)
            self._addImageActions(menu, media)

        if editable:
            self._separator(menu)
            self._addEditActions(menu)
        elif selected:
            self._separator(menu)
            self._addSelectionActions(menu, selected)

        if menu.isEmpty():
            self._addPageActions(menu)

        self._trimTrailingSeparator(menu)
        menu.popup(event.globalPos())

    # ------------------------------------------------------------------
    # Gruppi di voci
    # ------------------------------------------------------------------
    def _addLinkActions(self, menu: QMenu, link: QUrl):
        self._add(menu, "Open Link in a New Tab",
                  lambda u=link: self.linkNewTabRequested.emit(u))
        self._add(menu, "Open Link in a New Window",
                  lambda u=link: self.linkNewWindowRequested.emit(u))
        menu.addSeparator()
        self._std(menu, W.CopyLinkToClipboard)
        self._add(menu, "Copy Link without Trackers",
                  lambda u=link: self._copyText(clean_url(u).toString()))
        self._std(menu, W.DownloadLinkToDisk)           # passa da downloadRequested

    def _addImageActions(self, menu: QMenu, media: QUrl):
        self._add(menu, "Open Image in a New Tab",
                  lambda u=media: self.linkNewTabRequested.emit(u))
        self._std(menu, W.DownloadImageToDisk)          # "Save image as..."
        self._std(menu, W.CopyImageToClipboard)
        self._std(menu, W.CopyImageUrlToClipboard)

    def _addEditActions(self, menu: QMenu):
        self._std(menu, W.Undo)
        self._std(menu, W.Redo)
        menu.addSeparator()
        self._std(menu, W.Cut)
        self._std(menu, W.Copy)
        self._std(menu, W.Paste)
        menu.addSeparator()
        self._std(menu, W.SelectAll)

    def _addSelectionActions(self, menu: QMenu, selected: str):
        self._std(menu, W.Copy)
        short = selected[:30] + ("…" if len(selected) > 30 else "")
        # Nel testo della voce il "&" sarebbe letto come scorciatoia: lo raddoppio
        label = f"Search for “{short}”".replace("&", "&&")
        self._add(menu, label, lambda t=selected: self.searchRequested.emit(t))
        menu.addSeparator()
        self._std(menu, W.SelectAll)

    def _addPageActions(self, menu: QMenu):
        self._std(menu, W.Back)
        self._std(menu, W.Forward)
        self._std(menu, W.Reload)
        menu.addSeparator()
        # Il salvataggio passa dalla main window, che ha già il suo dialogo
        self._add(menu, "Save Page As…", self.savePageRequested.emit)
        self._std(menu, W.ViewSource)
        menu.addSeparator()
        self._std(menu, W.SelectAll)

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    def _std(self, menu: QMenu, web_action):
        """Aggiunge un'azione standard della pagina (si abilita/disabilita da sola)."""
        menu.addAction(self.pageAction(web_action))

    def _add(self, menu: QMenu, text: str, callback):
        """Aggiunge una voce personalizzata. 'triggered' invia un bool: lo ignoro."""
        action = menu.addAction(text)
        action.triggered.connect(lambda _checked=False: callback())
        return action

    @staticmethod
    def _separator(menu: QMenu):
        """Separatore solo se serve (menu non vuoto e ultima voce non già un separatore)."""
        actions = menu.actions()
        if actions and not actions[-1].isSeparator():
            menu.addSeparator()

    @staticmethod
    def _trimTrailingSeparator(menu: QMenu):
        actions = menu.actions()
        if actions and actions[-1].isSeparator():
            menu.removeAction(actions[-1])

    @staticmethod
    def _copyText(text: str):
        QGuiApplication.clipboard().setText(text)