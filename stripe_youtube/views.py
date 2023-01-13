from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


import stripe
stripe.api_key = "sk_test_51Lx8w7FIEDXjR5hTWLXSDlj3WXjJ9S8MFzUkn7j5ryXjACD2wnrsqtS5PRgteBsqsHEaolhg2q8O6b1N2li2x7th00tyRQzOf2"



def stripePay(request):
   if request.method == "POST":
                amount = int(request.POST["amount"]) 
                #Create customer
                try:
                        customer = stripe.Customer.create(
			                           email=request.POST.get("email"),
			                           name=request.POST.get("full_name"),
			                           description="Test donation",
                                    source=request.POST['stripeToken']
			                           )

                except stripe.error.CardError as e:
                  return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))     

                except stripe.error.RateLimitError as e:
                     # handle this e, which could be stripe related, or more generic
                     return HttpResponse("<h1>Rate error!</h1>")

                except stripe.error.InvalidRequestError as e:
                  return HttpResponse("<h1>Invalid requestor!</h1>")

                except stripe.error.AuthenticationError as e:  
                  return HttpResponse("<h1>Invalid API auth!</h1>")

                except stripe.error.StripeError as e:  
                  return HttpResponse("<h1>Stripe error!</h1>")

                except Exception as e:  
                  pass  



                #Stripe charge 
                charge = stripe.Charge.create(
                       customer=customer,
			              amount=int(amount)*100,
			              currency='usd',
			              description="Test donation"
                     ) 
                transRetrive = stripe.Charge.retrieve(
                           charge["id"],
                           api_key="sk_test_51Lx8w7FIEDXjR5hTWLXSDlj3WXjJ9S8MFzUkn7j5ryXjACD2wnrsqtS5PRgteBsqsHEaolhg2q8O6b1N2li2x7th00tyRQzOf2"
                        )
                charge.save() # Uses the same API Key.
                return redirect("pay_success/")

                   


   return render(request, "index.html")


def paysuccess(request):
    return render(request, "success.html")   
                