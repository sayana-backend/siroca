# import os
#
# import pandas import pd
# from django.http import HttpResponse
#
# from apps.application.models import ApplicationForm
# from .filter import ApplicationFilter
#
# def export_to_exel(request, self):
#     queryset = ApplicationFilter(request.GET, queryset=ApplicationForm.objects.all()).qs
#
#     df = pd.DataFrame(list(queryset.values()))
#
#     exel_file_path = os.path.join(os.path.dirname(__file__),f'report{self.}.xlsx')
#
#     response = HttpResponse(content_type=)
#