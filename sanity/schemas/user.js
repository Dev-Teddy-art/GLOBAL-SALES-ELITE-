export default {
  name: 'user',
  title: 'User (Network Node)',
  type: 'document',
  fields: [
    {
      name: 'email',
      title: 'Email',
      type: 'string',
    },
    {
      name: 'displayName',
      title: 'Display Name',
      type: 'string',
    },
    {
      name: 'role',
      title: 'Role',
      type: 'string',
      options: {
        list: [
          { title: 'Admin', value: 'admin' },
          { title: 'User', value: 'user' }
        ],
        layout: 'radio'
      }
    },
    {
      name: 'sponsorId',
      title: 'Sponsor ID (Referral Code)',
      type: 'string',
    },
    {
      name: 'referralCode',
      title: 'Referral Code',
      type: 'string',
    },
    {
      name: 'lft',
      title: 'Left Bound (Nested Set)',
      type: 'number',
    },
    {
      name: 'rgt',
      title: 'Right Bound (Nested Set)',
      type: 'number',
    },
    {
      name: 'payoutApproved',
      title: 'Payout Approved',
      type: 'boolean',
      initialValue: false,
    }
  ]
};
