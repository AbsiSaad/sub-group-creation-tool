// Copyright (c) 2025, Frappe Technologies and contributors
// For license information, please see license.txt

// Client side script for the Sub Group Creation Tool.
//
// This script wires up the form fields to server side methods
// defined on the SubGroupCreationTool DocType. When the user
// selects a main group, the program and academic year/term fields
// are automatically populated. The "Get Students" button fetches
// the relevant students based on the selected criteria and
// populates the child table. "Clear Students" removes all
// existing rows from the child table.

frappe.ui.form.on("Sub Group Creation Tool", {
    main_group: function (frm) {
        if (frm.doc.main_group) {
            frm.call({
                method: "load_main_group_details",
                doc: frm.doc,
                freeze: true,
                callback: function () {
                    frm.refresh_fields(["program", "academic_year", "academic_term"]);
                },
            });
        }
    },
    get_students_btn: function (frm) {
        frm.call({
            method: "fetch_students",
            doc: frm.doc,
            freeze: true,
            callback: function (r) {
                if (r.message) {
                    // Clear any existing rows
                    frm.clear_table("students");
                    // Populate with returned students
                    (r.message || []).forEach(function (d) {
                        let row = frm.add_child("students");
                        row.student = d.student;
                        row.student_name = d.student_name;
                        row.active = d.active;
                    });
                    frm.refresh_field("students");
                }
            },
        });
    },
    clear_students_btn: function (frm) {
        frm.call({
            method: "clear_students",
            doc: frm.doc,
            freeze: true,
            callback: function () {
                frm.refresh_field("students");
            },
        });
    },
});
