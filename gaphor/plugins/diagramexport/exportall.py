import logging
from pathlib import Path

from gaphor.core import gettext
from gaphor.core.modeling import Diagram
from gaphor.diagram.export import escape_filename
from gaphor.ui.statuswindow import StatusWindow

log = logging.getLogger(__name__)


def pkg2dir(package):
    """Return directory path from package class."""
    name: list[str] = []
    while package:
        name.insert(0, package.name)
        package = package.owningPackage
    return "/".join(name)


def export_all(factory, path, save_fn, suffix, name_re=None, underscore=None):
    diagrams = list(factory.select(Diagram))
    n_diagrams = len(diagrams)
    step = int(100 / n_diagrams)
    status_window = StatusWindow(
        title=gettext("Exporting all Diagrams..."),
        message=gettext(f"Exporting {n_diagrams} Diagrams...").format(
            n_diagrams=n_diagrams
        ),
        # parent=self.parent_window,
    )
    progress = 0
    for diagram in diagrams:
        odir = f"{path}/{pkg2dir(diagram.owner)}"
        # just diagram name
        dname = escape_filename(diagram.name)
        # full diagram name including package path
        pname = f"{odir}/{dname}"

        if underscore:
            log.info("replacing underscores")
            odir = odir.replace(" ", "_")
            dname = dname.replace(" ", "_")

        if name_re and not name_re.search(pname):
            log.debug("skipping %s", pname)
            continue

        outfilename = f"{odir}/{dname}.{suffix}"

        if not Path(odir).exists():
            log.debug("creating dir %s", odir)
            Path(odir).mkdir(parents=True)

        log.info("rendering: %s -> %s...", pname, outfilename)
        progress += step
        log.debug(progress)
        status_window.progress_synch(progress)
        # sleep(0.1)
        save_fn(outfilename, diagram)
    status_window.done()
