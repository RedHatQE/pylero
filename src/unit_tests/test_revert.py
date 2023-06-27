import pysvn
from pylero.project import Project
from pylero.test_run import TestRun

REVERT_TO = 2590
# this is the svn revision that the project should be reverted to for a clean
# environment. If anything required by the tests is added to the project, it
# must be manually cleaned and this number must be updated.


def revert_svn():
    proj = Project(Project.default_project)
    proj_grp = proj.project_group.name
    svn_url = "%s/%s/%s" % (proj.repo, proj_grp, proj.project_id)
    LOCAL_DIR = "/tmp/%s" % proj.project_id
    USER = proj.logged_in_user_id
    PASS = proj.session.password
    svn = pysvn.Client()
    svn.set_default_username(USER)
    svn.set_default_password(PASS)
    svn.set_store_passwords(False)
    svn.checkout(svn_url, LOCAL_DIR)
    svn_log = svn.log(LOCAL_DIR)
    #    first_revision = svn_log[-1].revision
    for log in svn_log:
        if log.revision.number == REVERT_TO:
            break
    first_revision = log.revision
    last_revision = svn_log[0].revision
    svn.merge(LOCAL_DIR, last_revision, LOCAL_DIR, first_revision, LOCAL_DIR)
    svn.checkin(LOCAL_DIR, "revert to original version")
    # The original Example template query has an extra colon.
    # After revert, must fix that.
    tmpl = TestRun(project_id=proj.project_id, test_run_id="Example")
    tmpl.query = tmpl.query.replace("::", ":")
    tmpl.update()


if __name__ == "__main__":
    revert_svn()
