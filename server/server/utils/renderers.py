from django.core.exceptions import ImproperlyConfigured
from rest_framework_csv.renderers import CSVRenderer


class GenericCSVRenderer(CSVRenderer):
    results_field = "results"
    fields = []

    def delete_keys_from_dict(self, orig_dict, keys_whitelist):
        """
        recursively delete keys which are not in whitelist from dict
        """
        for k in list(orig_dict.keys()):
            if k not in keys_whitelist:
                del orig_dict[k]

        for v in orig_dict.values():
            if isinstance(v, dict):
                self.delete_keys_from_dict(v, keys_whitelist)

        return orig_dict

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        """
        extract the array from results field & remove fields which were not specified in whitelist
        """
        if not self.fields:
            raise ImproperlyConfigured("fields attribute must be specified")
        results = data.get(self.results_field, [])
        if results:
            # Delete nested fields from objects.
            data = [self.delete_keys_from_dict(obj, self.fields) for obj in results]
        return super().render(data, media_type, renderer_context)
