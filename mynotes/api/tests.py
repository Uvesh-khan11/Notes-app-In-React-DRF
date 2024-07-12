from django.test import TestCase

# Create your tests here.
@api_view(["POST"])
# For Generate Invoice
def generateInvoice(request, id):
    try:
        if request.method == "POST":
            token = request.query_params.get('token')
            if token:
                url = BASE_URL + "api/token/verify/"
                headers = {"Authorization":f"bearer {token}"}
                body = {"token":token}
                result = requests.post(url, data=body, headers=headers)
                if result.status_code == 200:
                    decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
                    token_user_id = decoded_token["user_id"]
                    try:
                        user = CustomUser.objects.get(id=token_user_id)
                    except:
                        user = None
                        return JsonResponse({"Error": "User Not Found"})
                    # Invoice Template
                    template_path = "invoice_template.html"
                    # Get Object 
                    cab = CabBooking.objects.get(id=id)
                    if cab.user.id != user.id or not user.is_superuser:
                        return JsonResponse({"Error": "Authentication failed"})
                    # Generate Context
                    context = {
                        'cab_id': cab.booking_id,
                        'invoice_id': "CBIV" + str(datetime.now().strftime("%Y%m%d")) + str(cab.id),
                        'date': str(datetime.now().strftime("%d/%m/%Y")),
                    }
                    user_address = body.get('user_address',None)
                    if user_address: context["user_address"] = user_address
                    if cab.mobile: context["mobile_no"] = cab.mobile
                    if cab.name: context["name"] = cab.name
                    if cab.email: context["user_email"] = cab.email
                    if cab.pickup_address: context["pickup_address"] = cab.pickup_address
                    if cab.city: context["city"] = cab.city
                    if cab.pickup_time: context["pickup_time"] = cab.pickup_time
                    if cab.destination_cities: context["destination_cities"] = cab.destination_cities
                    if cab.luggage_space: context["luggage_space"] = cab.luggage_space
                    if cab.pickup_date: context["from_date"] = cab.pickup_date
                    if cab.return_date: context["to_date"] = cab.return_date
                    if cab.distance: context["distance"] = cab.distance
                    if cab.cab_method: context["cab_method"] = cab.cab_method
                    if cab.rental_option: context["rental_option"] = cab.rental_option
                    if cab.car: context["car"] = cab.car
                    if cab.booking_time: context["booking_time"] = cab.booking_time
                    if cab.booking_status: context["booking_status"] = cab.booking_status
                    if cab.payment_option: context["payment_option"] = cab.payment_option
                    if cab.payment_status: context["payment_status"] = cab.payment_status
                    if cab.advance_amount: context["advance_amount"] = cab.advance_amount
                    # if cab.remaining_amount: context["remaining_amount"] = cab.remaining_amount
                    # if cab.total_amount: context["total_amount"] = cab.total_amount
                    # if cab.gst: context["gst"] = cab.gst
                    # if cab.sub_total: context["sub_total"] = cab.sub_total
                    data = json.loads(request.body)
                    extra_km = safe_int(data.get("km"))
                    toll_tax = safe_int(data.get("toll_tax"))
                    border_tax = safe_int(data.get("border_tax"))
                    extra_pickup_drop_charges = safe_int(data.get("extra_pickup_drop_charges"))
                    parking_charges = safe_int(data.get("parking_charges"))
                    description = data["description"]
                    user_gst_no = data["gst_no"]
                    rates = {
                        "hatchback":{"ONE WAY":10,"ROUND TRIP":10,"LOCAL RENTAL":10,"AIRPORT":10},
                        "sedan": {"ONE WAY":11,"ROUND TRIP":11,"LOCAL RENTAL":11,"AIRPORT":11},
                        "suv": {"ONE WAY":14,"ROUND TRIP":14,"LOCAL RENTAL":14,"AIRPORT":14},
                        "premium suv": {"ONE WAY":18,"ROUND TRIP":18,"LOCAL RENTAL":18,"AIRPORT":18},
                    }
                    extra_charges = 0.0
                    try:
                        car_rate = rates[cab.car][cab.cab_method]
                        extra_charges += extra_km * car_rate
                        if toll_tax:
                            extra_charges += toll_tax
                        if border_tax:
                            extra_charges += border_tax
                        if parking_charges:
                            extra_charges += parking_charges
                        if extra_pickup_drop_charges:
                            extra_charges += extra_pickup_drop_charges
                        if user_gst_no: context["user_gst_no"] = user_gst_no
                        if description: context["description"] = description
                        if extra_charges != 0: context["extra_charges"] = extra_charges
                        if parking_charges != 0: context["parking_charges"] = parking_charges
                        if border_tax != 0: context["border_tax"] = border_tax
                        if toll_tax != 0: context["toll_tax"] = toll_tax
                        if extra_pickup_drop_charges != 0: context["extra_pickup_drop_charges"] = extra_pickup_drop_charges
                    except KeyError as e:
                        print("Invalid car type or method",str(e))
                    total_amount = cab.total_amount + extra_charges
                    gst = round(total_amount * 0.05)
                    context["amount"] = round(float(total_amount) - float(gst))
                    context["total_amount"] = total_amount
                    context["advance"] = cab.advance_amount
                    context["gst"] = gst
                    grand_total = round(float(total_amount) - float(cab.advance_amount))
                    context["grand_total"] = grand_total
                    # Generate Invoice
                    template = get_template(template_path)
                    html = template.render(context)

                    response = HttpResponse(content_type='application/pdf')
                    response["Content-Disposition"] = f'attachment; filename="CBWLIV{cab.id}.pdf"'
                    filename = f"CBWLIV{cab.id}.pdf"
                    
                    pisa_status = pisa.CreatePDF(html, dest=response)
                    if pisa_status.err:
                        return HttpResponse('Invoice generation failed')
                    # Save Invoice
                    cab.invoice.save(filename, File(BytesIO(response.content)))
                    # Restore Invoice
                    return response
                else:
                    return JsonResponse({"Error": "Authentication failed"})    
            else:
                return JsonResponse({"Error": "Authentication failed"})
        else:
            return JsonResponse({"Frobidden":"Method not Allowed"})
    except Exception as e:
        return JsonResponse({"Error":f" Something went wrong : {str(e)}"})