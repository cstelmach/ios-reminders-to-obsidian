def group_child_tasks_by_parent(child_tasks):
    child_tasks_by_parent_uuid = {}
    for task in child_tasks:
        parent_uuid = task["parent_uuid"]
        if parent_uuid not in child_tasks_by_parent_uuid:
            child_tasks_by_parent_uuid[parent_uuid] = []
        child_tasks_by_parent_uuid[parent_uuid].append(task)
    return child_tasks_by_parent_uuid