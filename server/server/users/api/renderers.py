from server.utils.renderers import GenericCSVRenderer


class UsersCSVRenderer(GenericCSVRenderer):
    fields = ["name", "email", "gender"]

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        """
        flatten profile nested fields
        """
        results = data.get(self.results_field, [])
        if results:
            results = [
                {
                    **{k: v for k, v in obj.items() if k != "profile"},
                    **(
                        {"gender": obj["profile"]["gender"]} if "profile" in obj else {}
                    ),
                }
                for obj in results
            ]
            # re-assign the results
            data[self.results_field] = results
        return super().render(data, media_type, renderer_context)
