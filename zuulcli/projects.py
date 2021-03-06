import logging

from cliff import lister
from cliff import show

from zuulcli import utils

LOG = logging.getLogger(__name__)


class ProjectsList(lister.Lister):
    """show projects list info of Zuul.
    """
    headers = ('Name', 'Canonical Name', 'Type')
    properties = ('name', 'canonical_name', 'type')

    def take_action(self, parsed_args):

        url = '/projects'
        resp = self.app.http_request(url)
        values = [[b.get(p, '') for p in self.properties] for b in resp.json()]
        return self.headers, values


class ProjectShow(show.ShowOne):
    """show one project info from Zuul API.
    """

    def get_parser(self, prog_name):
        parser = super(ProjectShow, self).get_parser(prog_name)
        parser.add_argument('project',
                            help='specified project name to show',
                            )
        return parser

    def take_action(self, parsed_args):
        resp = self.app.http_request('/project/%s' % parsed_args.project).json()
        values = []
        for value in resp.values():
            if isinstance(value, list) or isinstance(value, dict):
                values.append(utils.DictListColumn(value))
            else:
                values.append(value)
        return tuple(resp.keys()), tuple(values)
