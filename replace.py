import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

new_functions = """
  const initializeNewUser = async (currentUser: any, sponsorId: string, extraData: Partial<UserProfile>) => {
    const docRef = doc(db, 'users', currentUser.uid);
    
    let finalRole = 'user';
    let finalSponsorId = sponsorId || 'admin';

    if (currentUser.email === 'mypropteeapp@gmail.com') {
      finalRole = 'admin';
      finalSponsorId = 'admin';
    }

    let parentRgt = 0;
    let newLft = 1;
    let newRgt = 2;

    if (finalSponsorId !== 'admin') {
       const parentQuery = query(collection(db, 'users'), where('referralCode', '==', finalSponsorId), limit(1));
       const parentDocs = await getDocs(parentQuery);
       
       if (!parentDocs.empty) {
           parentRgt = (parentDocs.docs[0].data() as UserProfile).rgt || 0;
       } else {
           const parentByIdSnap = await getDoc(doc(db, 'users', finalSponsorId));
           if (parentByIdSnap.exists()) {
               parentRgt = (parentByIdSnap.data() as UserProfile).rgt || 0;
           } else {
               const maxRgtQuery = query(collection(db, 'users'), orderBy('rgt', 'desc'), limit(1));
               const maxRgtDocs = await getDocs(maxRgtQuery);
               if (!maxRgtDocs.empty) {
                   parentRgt = ((maxRgtDocs.docs[0].data() as UserProfile).rgt || 0) + 1;
               }
           }
       }
    } else {
       const maxRgtQuery = query(collection(db, 'users'), orderBy('rgt', 'desc'), limit(1));
       const maxRgtDocs = await getDocs(maxRgtQuery);
       if (!maxRgtDocs.empty) {
           parentRgt = ((maxRgtDocs.docs[0].data() as UserProfile).rgt || 0) + 1;
       }
    }

    const batch = writeBatch(db);
    const updates = new Map<string, any>();

    if (parentRgt > 0) {
        newLft = parentRgt;
        newRgt = parentRgt + 1;
        
        const shiftLftQuery = query(collection(db, 'users'), where('lft', '>', parentRgt));
        const shiftLftDocs = await getDocs(shiftLftQuery);
        shiftLftDocs.forEach(d => {
            updates.set(d.id, { ...updates.get(d.id), lft: increment(2) });
        });
        
        const shiftRgtQuery = query(collection(db, 'users'), where('rgt', '>=', parentRgt));
        const shiftRgtDocs = await getDocs(shiftRgtQuery);
        shiftRgtDocs.forEach(d => {
            updates.set(d.id, { ...updates.get(d.id), rgt: increment(2) });
        });
    }

    updates.forEach((updateData, id) => {
        batch.update(doc(db, 'users', id), updateData);
    });
    
    const newProfile: UserProfile = {
      email: extraData?.email || currentUser.email || '',
      displayName: currentUser.displayName || `${extraData?.firstName || ''} ${extraData?.lastName || ''}`.trim() || '',
      role: finalRole as 'admin' | 'user',
      isAdmin: finalRole === 'admin',
      sponsorId: finalSponsorId,
      referralCode: Math.random().toString(36).substring(2, 8).toUpperCase(),
      createdAt: serverTimestamp(),
      lastLoginAt: serverTimestamp(),
      lft: newLft,
      rgt: newRgt,
      firstName: extraData?.firstName || '',
      lastName: extraData?.lastName || '',
      address: extraData?.address || '',
      bankAccountNumber: extraData?.bankAccountNumber || '',
      bankAccountName: extraData?.bankAccountName || '',
      bankName: extraData?.bankName || '',
    };
    
    batch.set(docRef, newProfile);
    
    if (finalRole === 'admin') {
      const adminRef = doc(db, 'admins', currentUser.uid);
      batch.set(adminRef, {});
    }

    await batch.commit();
    setProfile(newProfile);
  };

  const signInWithGoogle = async (sponsorId: string = '', isLoginOnly: boolean = false, extraData?: Partial<UserProfile>) => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const currentUser = result.user;
      
      const docRef = doc(db, 'users', currentUser.uid);
      const docSnap = await getDoc(docRef);
      
      if (!docSnap.exists()) {
        if (isLoginOnly) {
          await firebaseSignOut(auth);
          throw {
            message: 'auth/user-not-found',
            email: currentUser.email,
            displayName: currentUser.displayName
          };
        }
        await initializeNewUser(currentUser, sponsorId, extraData || {});
      } else {
        setProfile(docSnap.data() as UserProfile);
      }
    } catch (error: any) {
      if (error?.message !== 'auth/user-not-found' && error?.code !== 'auth/popup-closed-by-user') {
        console.error("Error signing in with Google", error);
      }
      throw error;
    }
  };

  const signUpWithEmail = async (password: string, extraData: Partial<UserProfile>) => {
    try {
      const result = await createUserWithEmailAndPassword(auth, extraData.email!, password);
      await initializeNewUser(result.user, extraData.sponsorId || '', extraData);
    } catch (error: any) {
      console.error("Error signing up with email", error);
      throw error;
    }
  };

  const signInWithEmail = async (email: string, password: string) => {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      const docRef = doc(db, 'users', result.user.uid);
      const docSnap = await getDoc(docRef);
      if (docSnap.exists()) {
        setProfile(docSnap.data() as UserProfile);
      }
    } catch (error: any) {
      console.error("Error signing in with email", error);
      throw error;
    }
  };
"""

content = re.sub(r'  const signIn = async .*?^  const signOut = async \(\) => {', new_functions + '\n  const signOut = async () => {', content, flags=re.MULTILINE|re.DOTALL)
content = content.replace('signIn, signOut', 'signInWithGoogle, signUpWithEmail, signInWithEmail, signOut')

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
