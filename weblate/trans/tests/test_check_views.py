# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Test for check views."""

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from weblate.trans.tests.test_views import FixtureTestCase


class ChecksViewTest(FixtureTestCase):
    """Testing of check views."""
    def test_browse(self):
        response = self.client.get(reverse('checks'))
        self.assertContains(response, '/same/')

        response = self.client.get(reverse('checks'), {'language': 'de'})
        self.assertContains(response, '/same/')

        response = self.client.get(
            reverse('checks'),
            {'project': self.project.slug}
        )
        self.assertContains(response, '/same/')

    def test_check(self):
        response = self.client.get(
            reverse('show_check', kwargs={'name': 'same'})
        )
        self.assertContains(response, '/same/')

        response = self.client.get(
            reverse('show_check', kwargs={'name': 'ellipsis'})
        )
        self.assertContains(response, '…')

        response = self.client.get(
            reverse('show_check', kwargs={'name': 'not-existing'})
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            reverse('show_check', kwargs={'name': 'same'}),
            {'project': self.project.slug}
        )
        self.assertRedirects(
            response,
            reverse(
                'show_check_project',
                kwargs={'name': 'same', 'project': self.project.slug}
            )
        )
        response = self.client.get(
            reverse('show_check', kwargs={'name': 'same'}),
            {'language': 'de'}
        )
        self.assertContains(
            response,
            '/checks/same/test/?language=de'
        )

    def test_project(self):
        response = self.client.get(
            reverse(
                'show_check_project',
                kwargs={'name': 'same', 'project': self.project.slug}
            )
        )
        self.assertContains(response, '/same/')

        response = self.client.get(
            reverse(
                'show_check_project',
                kwargs={'name': 'same', 'project': self.project.slug}
            ),
            {'language': 'cs'}
        )
        self.assertContains(response, '/same/')

        response = self.client.get(
            reverse(
                'show_check_project',
                kwargs={'name': 'ellipsis', 'project': self.project.slug}
            )
        )
        self.assertContains(response, '…')

        response = self.client.get(
            reverse(
                'show_check_project',
                kwargs={'name': 'non-existing', 'project': self.project.slug}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_subproject(self):
        response = self.client.get(
            reverse(
                'show_check_subproject',
                kwargs={
                    'name': 'same',
                    'project': self.project.slug,
                    'subproject': self.subproject.slug,
                }
            )
        )
        self.assertContains(response, '/same/')

        response = self.client.get(
            reverse(
                'show_check_subproject',
                kwargs={
                    'name': 'ellipsis',
                    'project': self.project.slug,
                    'subproject': self.subproject.slug,
                }
            )
        )
        self.assertRedirects(
            response,
            '{0}?type=check%3Aellipsis'.format(
                reverse('review_source', kwargs={
                    'project': self.project.slug,
                    'subproject': self.subproject.slug,
                })
            )
        )

        response = self.client.get(
            reverse(
                'show_check_subproject',
                kwargs={
                    'name': 'non-existing',
                    'project': self.project.slug,
                    'subproject': self.subproject.slug,
                }
            )
        )
        self.assertEqual(response.status_code, 404)
