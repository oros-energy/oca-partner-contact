# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test companies created without Tax ID."""

from odoo.tests import TransactionCase


class TestCompanyWithoutVat(TransactionCase):
    def _create_company(self, **extra):
        return self.env["res.partner"].create(
            {"name": "Sôme Company", "is_company": True, **extra}
        )

    def test_create_company_without_vat(self):
        company = self._create_company()
        self.assertTrue(company.is_company)
        self.assertFalse(company.has_vat)
        # A company keeps its full name, it is not split
        self.assertEqual(company.name, "Sôme Company")
        self.assertEqual(company.lastname, "Sôme Company")
        self.assertFalse(company.firstname)

    def test_company_survives_recomputation(self):
        company = self._create_company()
        # Changing the Tax ID recomputes is_company
        company.vat = "/"
        self.env.flush_all()
        self.assertTrue(company.is_company)
        company.vat = False
        self.env.flush_all()
        self.assertTrue(company.is_company)
        self.assertEqual(company.name, "Sôme Company")

    def test_company_with_parent_is_not_a_company(self):
        parent = self._create_company()
        company = self._create_company(name="Sôme Subsidiary")
        company.parent_id = parent
        self.env.flush_all()
        self.assertFalse(company.is_company)

    def test_explicit_person_stays_person(self):
        person = self.env["res.partner"].create(
            {"firstname": "Fïrst", "lastname": "Läst", "is_company": False}
        )
        person.vat = "/"
        self.env.flush_all()
        self.assertFalse(person.is_company)
        self.assertEqual(person.firstname, "Fïrst")

    def test_company_from_vat(self):
        company = self.env["res.partner"].create(
            {"name": "Sôme Company", "vat": "BE0477472701"}
        )
        self.assertTrue(company.is_company)
        self.assertEqual(company.lastname, "Sôme Company")
