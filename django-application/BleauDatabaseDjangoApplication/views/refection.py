####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) Salvaire Fabrice 2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import json

####################################################################################################

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

####################################################################################################

from ..models import Circuit, Person, Refection

####################################################################################################

class RefectionForm(ModelForm):

    class Meta:
        model = Refection
        fields = (
            'circuit',
            'date',
            'note'
            )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(RefectionForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def create(request, circuit_id):

    circuit = get_object_or_404(Circuit, pk=circuit_id)

    if request.method == 'POST':
        form = RefectionForm(request.POST)
        if form.is_valid():
            refection = form.save(commit=False)
            refection.save()
            messages.success(request, _("Refection créé avec succès."))
            return HttpResponseRedirect(reverse('refection.details', args=[refection.pk]))
        else:
            messages.error(request, _("Des informations sont manquantes ou incorrectes"))
    else:
        form = RefectionForm(initial={'circuit': circuit})

    return render(request, 'refection/create.html', {'form': form, 'circuit': circuit})

####################################################################################################

@login_required
def details(request, refection_id):

    refection = get_object_or_404(Refection, pk=refection_id)
    return render(request, 'refection/details.html', {'refection': refection})

####################################################################################################

@login_required
def update(request, refection_id):

    refection = get_object_or_404(Refection, pk=refection_id)

    if request.method == 'POST':
        form = RefectionForm(request.POST, instance=refection)
        if form.is_valid():
            refection = form.save()
            return HttpResponseRedirect(reverse('refection.details', args=[refection.pk]))
    else:
        form = RefectionForm(instance=refection)

    return render(request, 'refection/create.html', {'form': form, 'update': True, 'refection': refection})

####################################################################################################

@login_required
def persons(request, refection_id):

    refection = get_object_or_404(Refection, pk=refection_id)

    person_data = [{'pk':person.pk, 'name':person.name} for person in Person.objects.all()] # last_first_
    person_data_json = json.dumps(person_data)

    return render(request, 'refection/persons.html', {'refection': refection, 'person_data': person_data_json})

####################################################################################################

@login_required
def delete(request, refection_id):

    refection = get_object_or_404(Refection, pk=refection_id)
    circuit = refection.circuit
    messages.success(request, _("Refection «{0.date}» supprimé").format(refection))
    refection.delete()

    return HttpResponseRedirect(reverse('circuit.details', args=[circuit.pk]))
