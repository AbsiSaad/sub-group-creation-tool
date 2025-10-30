# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

"""
This module contains the server side logic for the Sub Group Creation Tool.

The purpose of this DocType is to make it easy for education managers to
create "sub groups" beneath an existing Student Group. A sub group is a
collection of students filtered from a main group based on criteria such as
program, course, batch and instructor. The tool exposes a few helper
functions that fetch the relevant students from the main group and populate
the child table on the form.

The fields on the DocType correspond to the UI described in the design
sketch provided by the user. See sub_group_creation_tool.json for details.

Note: This DocType does not automatically persist newly created Student
Group documents; rather it prepares the data for creation. Actual sub
group creation can be performed in a custom script or extended as needed.
"""

import frappe
from frappe import _
from frappe.model.document import Document

from education.education.doctype.student_group.student_group import get_students as sg_get_students


class SubGroupCreationTool(Document):
    """Backend logic for the Sub Group Creation Tool DocType."""

    @frappe.whitelist()
    def load_main_group_details(self):
        """Populate program, academic year and term from the selected main group.

        When a user selects a main group, this method copies the program,
        academic year and academic term to the form. This ensures that
        downstream lookups (such as fetching students) use the correct
        context without requiring the user to re‑enter these details.
        """
        if not self.main_group:
            return

        # fetch the main Student Group and set defaults
        sg = frappe.get_doc("Student Group", self.main_group)
        self.program = sg.program
        self.academic_year = sg.academic_year
        self.academic_term = sg.academic_term

    @frappe.whitelist()
    def fetch_students(self):
        """Return a list of students based on the selected criteria.

        This function delegates to the existing `get_students` utility on
        `education.education.doctype.student_group.student_group`. It passes
        through the academic year/term, program and batch from the main
        group together with the selected group type (Course or Batch) to
        retrieve the applicable students.

        Returns:
            list[dict]: A list of student dicts suitable for populating
                the child table on the form.
        """
        if not self.academic_year or not self.group_type:
            frappe.throw(_("Please select a Main Group and Group Type before fetching students."))

        # Determine which grouping mode to use based on the user's selection.
        group_based_on = self.group_type

        students = sg_get_students(
            academic_year=self.academic_year,
            academic_term=self.academic_term,
            program=self.program,
            batch=self.sub_branch,
            student_category=None,
            course=self.course if group_based_on == "Course" else None,
        )

        return students

    @frappe.whitelist()
    def clear_students(self):
        """Clear any existing students from the child table.

        This helper makes it easy to reset the list before fetching a new
        selection of students. It iterates through the child table rows and
        removes them individually.
        """
        self.set("students", [])
