import os
import smtplib


def send_email(rss_feed, email_body, server):
    """Send email with properties that fit user paramters."""
    email_body = email_body.encode("ascii", "ignore")
    email_body = email_body.decode()

    with smtplib.SMTP(server, port=587) as connection:
        connection.starttls()
        connection.login(os.getenv("FROM_EMAIL"), os.getenv("EMAIL_PASSWORD"))
        connection.sendmail(
            from_addr=os.getenv("FROM_EMAIL"),
            to_addrs=os.getenv("TO_EMAIL"),
            msg=f"Subject:Property Listings\n\n{email_body}.",
        )

    print("Email has been sent")
