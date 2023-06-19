from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import redirect
from django.conf import settings
from .paytm_checksum import generate_checksum

def initiate_payment(request):
    # Generate unique order ID and amount for your transaction
    order_id = "<generate_unique_order_id>"
    amount = "<transaction_amount>"

    # Set other required parameters for the payment
    params = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': order_id,
        'CUST_ID': request.user.email,  # Use customer's email or any unique identifier
        'TXN_AMOUNT': str(amount),
        'CHANNEL_ID': 'WEB',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CALLBACK_URL': '<your_callback_url>',
    }

    # Generate checksum using the provided function
    checksum, salt = generate_checksum(params, settings.PAYTM_MERCHANT_KEY)

    # Add checksum and salt to the request parameters
    params['CHECKSUMHASH'] = checksum
    params['SALT'] = salt

    # Redirect the user to the Paytm payment page
    paytm_url = 'https://securegw-stage.paytm.in/theia/processTransaction'
    return redirect(paytm_url + '?' + urlencode(params))



from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .paytm_checksum import generate_checksum

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = request.POST
        received_checksum = data.get('CHECKSUMHASH')

        # Verify the checksum received in the response
        checksum, _ = generate_checksum(data, settings.PAYTM_MERCHANT_KEY)
        if checksum == received_checksum:
            # Check if the transaction is successful
            if data.get('RESPCODE') == '01':
                # Process the successful payment
                # Update your database or perform any necessary actions
                return HttpResponse('Payment success')
            else:
                # Handle payment failure
                return HttpResponse('Payment failed')
        else:
            # Handle checksum mismatch
            return HttpResponse('Checksum mismatch')
    else:
        return HttpResponse(status=400)
