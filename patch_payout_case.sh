sed -i "s/if (payoutStatus === 'paid') {/if (payoutStatus === 'paid' || payoutStatus === 'Paid' || payoutStatus?.toLowerCase() === 'paid') {/g" server.ts
