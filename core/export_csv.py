from core.exportutils import get_fk_value


def export_logentry_iterator(queryset):
    yield ["action_time", "user", "content_type", "action_flag_", "change_message"]
    for obj in queryset:
        yield [obj.action_time, obj.user, obj.content_type, obj.action_flag_, obj.change_message]