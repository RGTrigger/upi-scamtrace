from datetime import datetime, timezone, timedelta

def scenarios():
    now=datetime.now(timezone.utc)
    def ts(h): return (now-timedelta(hours=h)).isoformat()
    def case(title,summary,events,label): return {"title":title,"summary":"Synthetic demo: "+summary,"synthetic":True,"expected_risk":label,"events":events}
    def e(h,t,ch,text): return {"timestamp":ts(h),"event_type":t,"channel":ch,"content":text,"source":"synthetic-demo"}
    return [
      case("Fake Refund / Receive-Money Deception","refund claim followed by collect request.",[e(3,"message","SMS","A refund is ready. Approve the UPI collect request to receive your money."),e(1,"payment_request","UPI","Caller sent a collect request and said approval will credit the refund.")],"HIGH_CONCERN"),
      case("Fake Electricity KYC Scam","urgent cross-channel message, call, link, and payment request.",[e(5,"message","SMS","Electricity KYC will expire today. Update immediately at https://example.invalid/kyc"),e(3,"call_summary","Phone","Caller claimed to be electricity support and urged an immediate update."),e(1,"payment_request","UPI","Caller asked user to approve a collect request to receive refund.")],"HIGH_CONCERN"),
      case("Fake Bank KYC Support","support impersonation asks for a secret.",[e(2,"message","Chat","Bank KYC is urgent; share your OTP immediately to avoid account suspension."),e(1,"call_summary","Phone","Caller claiming bank support repeated the OTP request.")],"HIGH_CONCERN"),
      case("QR Payment Deception","synthetic QR payload presented for user review; user intent was not captured.",[e(1,"qr_payload","QR Code","upi://pay?pa=demo-payee@example&pn=Sample%20Merchant&am=250&cu=INR")],"INSUFFICIENT_EVIDENCE"),
      case("Repeated Payment Escalation","multiple collect requests with refund pressure.",[e(4,"payment_request","UPI","Approve this collect request to receive refund."),e(2,"payment_request","UPI","Second collect request; approve immediately to complete refund."),e(1,"payment_request","UPI","Another collect request was sent after the first failed.")],"HIGH_CONCERN"),
      case("Benign Rent Payment","known-context rent payment without pressure.",[e(2,"message","Chat","Rent transfer for April is due this week; please use the usual account."),e(1,"payment_attempt","UPI","User reports sending the agreed rent; not independently verified.")],"LOW_CONCERN"),
      case("Benign Merchant Payment","ordinary merchant payment with no urgent demand.",[e(2,"message","Chat","Lunch at Sample Cafe today."),e(1,"payment_attempt","UPI","User reports paying INR 320 at Sample Cafe; not independently verified.")],"LOW_CONCERN"),
      case("Ambiguous Incomplete Case","partial contact evidence with action and recipient missing.",[e(1,"note","Other","Someone called earlier. I do not remember the number or what they asked.")],"INSUFFICIENT_EVIDENCE"),
      case("False-Positive Challenge","time-sensitive delivery notice without corroboration.",[e(1,"message","SMS","Urgent delivery update: please check the order status in the official app.")],"CAUTION"),
      case("Multi-Channel Scam Journey","message to call to link to payment sequence.",[e(6,"message","SMS","KYC update is urgent today. Open https://example.invalid/account"),e(4,"call_summary","Phone","Caller claimed official support and told user to continue in chat."),e(2,"url","Chat","https://example.invalid/account was sent again with an immediate deadline."),e(1,"payment_request","UPI","Approve a collect request now to prevent a service suspension.")],"HIGH_CONCERN")
    ]
