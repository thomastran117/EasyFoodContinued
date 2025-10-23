from fastapi_mail import FastMail, MessageSchema, MessageType

from config.emailConfig import conf

frontend_url = "http://localhost:3050"


async def send_reservation_email(email: str, details):
    pass


async def send_order_email(email: str, details):
    pass


async def send_verification_email(email: str, token: str):
    verification_link = f"{frontend_url}/auth/verify?token={token}"
    subject = "Welcome to EasyFood! Please Verify Your Email"

    body = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="x-ua-compatible" content="ie=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Verify your email</title>
        </head>
        <body style="margin:0; padding:0; background-color:#f0f4f8;">
            <!-- Preheader (hidden preview text) -->
            <div style="display:none; max-height:0; overflow:hidden; opacity:0; mso-hide:all;">
            Confirm your email to finish setting up your EasyFood account.
            </div>

            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f0f4f8;">
            <tr>
                <td align="center" style="padding:24px 12px;">
                <!--[if mso]>
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600">
                    <tr><td>
                <![endif]-->
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.07);">
                    <!-- Header / Logo -->
                    <tr>
                    <td align="center" style="padding:32px 32px 8px 32px;">
                        <!-- Optional logo -->
                        <!-- <img src="https://your-cdn/logo.png" alt="EasyFood" width="120" style="display:block; border:0; outline:none; text-decoration:none;"> -->
                        <h1 style="margin:0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:24px; line-height:1.3; color:#0b63f6;">
                        Welcome to EasyFood!
                        </h1>
                        <p style="margin:8px 0 0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:16px; color:#556271;">
                        We're excited to have you on board 🎉
                        </p>
                    </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                    <td style="padding:0 32px;">
                        <hr style="border:0; border-top:1px solid #e6ecf3; margin:16px 0 0 0;">
                    </td>
                    </tr>

                    <!-- Body -->
                    <tr>
                    <td style="padding:24px 32px 8px 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#2b2f36; font-size:15px; line-height:1.6;">
                        <p style="margin:0 0 12px 0;">Hello,</p>
                        <p style="margin:0;">
                        Thanks for signing up! Please confirm your email address to get started.
                        </p>
                    </td>
                    </tr>

                    <!-- CTA Button (Bulletproof: works in Outlook) -->
                    <tr>
                    <td align="center" style="padding:24px 32px 8px 32px;">
                        <!--[if mso]>
                        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="{verification_link}" style="height:48px; v-text-anchor:middle; width:240px;" arcsize="12%" fillcolor="#0b63f6" strokecolor="#0b63f6">
                        <w:anchorlock/>
                        <center style="color:#ffffff; font-family:Segoe UI, Arial, sans-serif; font-size:16px; font-weight:bold;">
                            Verify Your Email
                        </center>
                        </v:roundrect>
                        <![endif]-->
                        <!--[if !mso]><!-- -->
                        <a href="{verification_link}"
                        style="display:inline-block; background-color:#0b63f6; color:#ffffff; text-decoration:none; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:16px; font-weight:700; line-height:48px; border-radius:6px; padding:0 24px; min-width:220px; text-align:center;">
                        Verify Your Email
                        </a>
                        <!--<![endif]-->
                    </td>
                    </tr>

                    <!-- Fallback link + note -->
                    <tr>
                    <td style="padding:12px 32px 4px 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#556271; font-size:13px; line-height:1.6;">
                        <p style="margin:0;">
                        If the button doesn’t work, copy and paste this link into your browser:
                        </p>
                        <p style="margin:8px 0 0; word-break:break-all;">
                        <a href="{verification_link}" style="color:#0b63f6; text-decoration:underline;">{verification_link}</a>
                        </p>
                    </td>
                    </tr>

                    <!-- Help / Safety -->
                    <tr>
                    <td style="padding:20px 32px 0 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#556271; font-size:13px; line-height:1.6;">
                        <p style="margin:0;">
                        Didn’t create an EasyFood account? You can safely ignore this email.
                        </p>
                    </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                    <td align="center" style="padding:28px 24px 32px 24px;">
                        <p style="margin:0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:12px; color:#98a5b3; line-height:1.6;">
                        © 2025 EasyFood, All rights reserved.
                        </p>
                        <!-- Optional small links
                        <p style="margin:6px 0 0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:12px; color:#98a5b3;">
                        <a href="https://yourdomain.example/preferences" style="color:#98a5b3; text-decoration:underline;">Email preferences</a> ·
                        <a href="https://yourdomain.example/privacy" style="color:#98a5b3; text-decoration:underline;">Privacy</a>
                        </p>
                        -->
                    </td>
                    </tr>
                </table>
                <!--[if mso]></td></tr></table><![endif]-->
                </td>
            </tr>
            </table>
        </body>
        </html>
        """

    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_forgot_password_email(email: str, token: str):
    reset_link = f"{frontend_url}/auth/change-password?token={token}"
    subject = "Reset your EasyFood password"

    body = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Reset your password</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f0f4f8;">
        <div style="display:none; max-height:0; overflow:hidden; opacity:0; mso-hide:all;">
            You requested to reset your EasyFood account password.
        </div>

        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f0f4f8;">
        <tr>
            <td align="center" style="padding:24px 12px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.07);">
                
                <!-- Header -->
                <tr>
                    <td align="center" style="padding:32px 32px 8px 32px;">
                        <h1 style="margin:0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:24px; color:#0b63f6;">
                            Reset Your Password
                        </h1>
                        <p style="margin:8px 0 0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:16px; color:#556271;">
                            A request was made to reset your EasyFood password.
                        </p>
                    </td>
                </tr>

                <tr>
                    <td style="padding:0 32px;">
                        <hr style="border:0; border-top:1px solid #e6ecf3; margin:16px 0 0 0;">
                    </td>
                </tr>

                <!-- Body -->
                <tr>
                    <td style="padding:24px 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#2b2f36; font-size:15px; line-height:1.6;">
                        <p style="margin:0 0 12px 0;">Hello,</p>
                        <p style="margin:0 0 12px 0;">
                            You recently requested to reset your EasyFood account password.
                            Click the button below to create a new password.
                        </p>
                        <p style="margin:0 0 12px 0;">
                            This link will expire in 1 hour for your security.
                        </p>
                    </td>
                </tr>

                <!-- CTA -->
                <tr>
                    <td align="center" style="padding:24px 32px 8px 32px;">
                        <a href="{reset_link}"
                        style="display:inline-block; background-color:#0b63f6; color:#ffffff; text-decoration:none; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:16px; font-weight:700; line-height:48px; border-radius:6px; padding:0 24px; min-width:220px; text-align:center;">
                            Reset Password
                        </a>
                    </td>
                </tr>

                <!-- Fallback link -->
                <tr>
                    <td style="padding:16px 32px 4px 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#556271; font-size:13px; line-height:1.6;">
                        <p style="margin:0;">
                            If the button doesn’t work, copy and paste this link into your browser:
                        </p>
                        <p style="margin:8px 0 0; word-break:break-all;">
                            <a href="{reset_link}" style="color:#0b63f6; text-decoration:underline;">{reset_link}</a>
                        </p>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td style="padding:20px 32px 0 32px; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color:#556271; font-size:13px; line-height:1.6;">
                        <p style="margin:0;">
                            If you didn’t request this, you can safely ignore this email.
                        </p>
                    </td>
                </tr>

                <tr>
                    <td align="center" style="padding:28px 24px 32px 24px;">
                        <p style="margin:0; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; font-size:12px; color:#98a5b3;">
                            © 2025 EasyFood, All rights reserved.
                        </p>
                    </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
