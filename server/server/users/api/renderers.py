from rest_framework_csv.renderers import CSVRenderer


class UsersCSVRenderer(CSVRenderer):
    results_field = "results"
    delete_fields = ["slug"]

    def delete_keys_from_dict(self, dict_del, lst_keys):
        """
        recursively delete keys from dict
        """
        for k in lst_keys:
            try:
                del dict_del[k]
            except KeyError:
                pass
        for v in dict_del.values():
            if isinstance(v, dict):
                self.delete_keys_from_dict(v, lst_keys)

        return dict_del

    def render(self, data, media_type=None, renderer_context=None):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
            # Delete nested fields from objects.
            data = [self.delete_keys_from_dict(obj, self.delete_fields) for obj in data]
            # TODO: Refactor, this is magic that convert profile to gender only
            data = [
                {
                    **{k: v for k, v in obj.items() if k != "profile"},
                    **(
                        {"gender": obj["profile"]["gender"]} if "profile" in obj else {}
                    ),
                }
                for obj in data
            ]
        return super(UsersCSVRenderer, self).render(data, media_type, renderer_context)
