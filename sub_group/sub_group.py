# Copyright (c) 2025, Education Module and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SubGroup(Document):
    def validate(self):
        """
        Ensure that a sub group with the same name does not already exist under the same parent group.
        """
        if self.parent_group and self.sub_group_name:
            existing = frappe.db.exists(
                "Sub Group",
                {
                    "parent_group": self.parent_group,
                    "sub_group_name": self.sub_group_name,
                    "name": ["!=", self.name],
                },
            )
            if existing:
                frappe.throw(
                    f"Sub Group with name '{self.sub_group_name}' already exists under the selected Parent Group."
                )

    @frappe.whitelist()
    def get_students(self, program=None, sub_branch=None, course=None):
        """
        Fetch students for this sub group based on optional filters.
        This method uses the helper from the Student Group DocType to reuse student fetch logic.
        :param program: Program to filter students by
        :param sub_branch: Batch or branch to filter students by
        :param course: Course to filter students by
        :return: List of student dicts matching the filters
        """
        filters = {}
        if program:
            filters["program"] = program
        if sub_branch:
            # In Student Group, batch field represents program batch/branch
            filters["batch"] = sub_branch
        if course:
            filters["course"] = course

        # Import and delegate to the existing get_students function from Student Group
        from education.education.doctype.student_group.student_group import get_students

        return get_students(filters)
