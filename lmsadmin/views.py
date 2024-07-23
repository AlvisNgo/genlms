import csv
import html
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm

def index(request):
	# Check if user is superadmin
	if not request.user.is_superuser:
		return HttpResponseForbidden("You do not have permission to access this page.")

	if request.method == 'POST':
		form = CSVUploadForm(request.POST, request.FILES)
		if form.is_valid():
			csv_file = form.cleaned_data['csv_file']
			decoded_file = csv_file.read().decode('utf-8').splitlines()
			reader = csv.DictReader(decoded_file)
			
			# Process all rows
			errors = []
			valid_rows = []
			
			for line_number, row in enumerate(reader, start=1):
				# Validate that all rows exist
				if not row['email'] or not row['first_name'] or not row['last_name']:
					errors.append((line_number, row, f"Row is missing one or more column."))
					continue
				
				# Escape the content to prevent XSS
				email = row['email'].strip()
				first_name = html.escape(row['first_name'].strip())
				last_name = html.escape(row['last_name'].strip())
				
				# Validate the email
				try:
					validate_email(email)
				except ValidationError:
					errors.append((line_number, row, f"Invalid email: {email}"))
					continue

				# No duplicate email within the csv itself
				if any(row['email'] == email for row in valid_rows):
					errors.append((line_number, row, f"Duplicate email within .csv file, only first one will be imported."))
					continue

				if User.objects.filter(email=email).exists():
					errors.append((line_number, row, f"User with email {email} already exists."))
					continue
				
				valid_rows.append({
					'username': email,
					'first_name': first_name,
					'last_name': last_name,
					'email': email
				})
			
			if errors or valid_rows:
				request.session['valid_rows'] = valid_rows
				return render(request, 'index_confirm.html', {
					'errors': errors,
					'valid_count': len(valid_rows)
				})
			else:
				return HttpResponse("No valid rows to import.")
	else:
		form = CSVUploadForm()

	return render(request, 'index.html', {'form': form})

def import_valid_rows(request):
	if request.method == 'POST':
		valid_rows = request.session.get('valid_rows', [])
		if 'proceed' in request.POST:
			if valid_rows:
				for row in valid_rows:
					User.objects.create(
						username=row['username'],
						first_name=row['first_name'],
						last_name=row['last_name'],
						email=row['email']
					)
				del request.session['valid_rows']
				messages.success(request, "Valid users imported successfully.")
			else:
				messages.warning(request, "No valid rows to import.")
		else:
			del request.session['valid_rows']
		return redirect('index')
	else:
		return redirect('index')