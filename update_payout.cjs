const fs = require('fs');
let code = fs.readFileSync('server.ts', 'utf8');

code = code.replace("import nodemailer from 'nodemailer';", "import { sendPayoutConfirmationEmail } from './src/lib/email.ts';");

const targetEndpoint = `      if (payoutStatus === 'paid' || payoutStatus === 'Paid' || payoutStatus?.toLowerCase() === 'paid') {
        try {
          const saleWithUser = await sanityClient.fetch(\`*[_type == "sale" && _id == $id][0] {
            ...,
            userRef->{email, displayName, firstName}
          }\`, { id: saleId });
          
          if (saleWithUser?.userRef?.email) {
            const userEmail = saleWithUser.userRef.email;
            const userName = saleWithUser.userRef.firstName || saleWithUser.userRef.displayName || 'Realtor';
            
            if (process.env.ZOHO_EMAIL_USER && process.env.ZOHO_EMAIL_PASS) {
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
                from: \`"Global Sales Elite" <\${process.env.ZOHO_EMAIL_USER}>\`,
                to: userEmail,
                subject: 'Commission Payout Confirmed! 🎉',
                html: \`<p>Hi \${userName},</p><p>Great news! Your commission payout of ₦\${(saleWithUser.amount || 0).toLocaleString()} for the sale of <strong>\${saleWithUser.propertyName || 'Property'}</strong> has been processed and paid.</p><p>Keep up the great work!</p><p>Best,<br/>Global Sales Elite Admin Team</p>\`
              });
              console.log(\`[Email] Payout confirmation email sent to \${userEmail} via Zoho Mail\`);
            } else {
              console.log(\`[Mock Email] Would send payout confirmation email to \${userEmail} for sale \${saleId}\`);
            }
          }
        } catch (emailErr) {
          console.error("Failed to send payout confirmation email:", emailErr);
        }
      }`;

const newEndpoint = `      if (payoutStatus === 'paid' || payoutStatus === 'Paid' || payoutStatus?.toLowerCase() === 'paid') {
        try {
          const saleWithUser = await sanityClient.fetch(\`*[_type == "sale" && _id == $id][0] {
            ...,
            userRef->{email, displayName, firstName}
          }\`, { id: saleId });
          
          if (saleWithUser?.userRef?.email) {
            const userEmail = saleWithUser.userRef.email;
            const userName = saleWithUser.userRef.firstName || saleWithUser.userRef.displayName || 'Realtor';
            const amount = saleWithUser.amount || 0;
            const propertyName = saleWithUser.propertyName || 'Property';
            
            await sendPayoutConfirmationEmail(userEmail, userName, amount, propertyName);
          }
        } catch (emailErr) {
          console.error("Failed to send payout confirmation email:", emailErr);
        }
      }`;

if (code.includes(targetEndpoint)) {
  code = code.replace(targetEndpoint, newEndpoint);
  fs.writeFileSync('server.ts', code);
  console.log("Successfully updated server.ts");
} else {
  console.log("Could not find the target endpoint to replace in server.ts");
}
