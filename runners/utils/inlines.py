class ReadOnlyFieldsMixin:
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if hasattr(self, "readonly_fields_update"):
                return self.readonly_fields_update
        else:
            if hasattr(self, "readonly_fields_create"):
                return self.readonly_fields_create
        return self.readonly_fields
