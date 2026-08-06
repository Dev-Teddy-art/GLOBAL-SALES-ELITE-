import nodemailer from 'nodemailer';

export const sendPayoutConfirmationEmail = async (
  userEmail: string,
  userName: string,
  amount: number,
  propertyName: string
) => {
  if (!process.env.ZOHO_EMAIL_USER || !process.env.ZOHO_EMAIL_PASS) {
    console.log(`[Mock Email] Would send payout confirmation email to ${userEmail} for sale of ${propertyName}`);
    return;
  }

  try {
    const transporter = nodemailer.createTransport({
      host: 'smtp.zoho.com',
      port: 465,
      secure: true,
      auth: {
        user: process.env.ZOHO_EMAIL_USER,
        pass: process.env.ZOHO_EMAIL_PASS,
      },
    });

    await transporter.sendMail({
      from: `"Global Sales Elite" <${process.env.ZOHO_EMAIL_USER}>`,
      to: userEmail,
      subject: 'Commission Payout Confirmed! 🎉',
      html: `<p>Hi ${userName},</p>
<p>Great news! Your commission payout of ₦${(amount || 0).toLocaleString()} for the sale of <strong>${propertyName || 'Property'}</strong> has been processed and paid.</p>
<p>Keep up the great work!</p>
<p>Best,<br/>Global Sales Elite Admin Team</p>`
    });
    console.log(`[Email] Payout confirmation email sent to ${userEmail} via Zoho Mail`);
  } catch (error) {
    console.error("Failed to send payout confirmation email:", error);
    throw error;
  }
};
