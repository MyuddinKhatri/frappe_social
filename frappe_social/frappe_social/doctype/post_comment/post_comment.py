# Copyright (c) 2018, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe.desk.notifications import extract_mentions
from frappe.model.document import Document


class PostComment(Document):
	def after_insert(self):
		mentions = extract_mentions(self.content)
		for mention in mentions:
			if mention == self.owner:
				continue
			frappe.publish_realtime(
				"mention",
				"""{} mentioned you!
				<br><a class="text-muted text-small" href="desk#social/home">Check Social<a>""".format(
					frappe.utils.get_fullname(self.owner)
				),
				user=mention,
				after_commit=True,
			)
		frappe.publish_realtime("new_post_comment" + self.post, self, after_commit=True)
