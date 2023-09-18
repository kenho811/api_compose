from tests.unit_tests.resources.views.base import BaseView


class StatelessView(BaseView):
    def search(self, number):
        resp = {'number': number}
        return self.dict_to_xml(resp) if self.is_xml() else resp, 200
