class DynamicTemplate:

    template_base_dir = ""  # Optionally define a subfolder to organize templates

    def get_template_names(self):

        model_name = self.model.__name__.lower()  # Get model name in lowercase
        action_suffix = getattr(self, "template_name_suffix", "")
        return [f"{self.template_base_dir}{model_name}/{model_name}{action_suffix}.html"]