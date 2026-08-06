import React, { useRef, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Camera, Loader2, Upload, X } from 'lucide-react';
import { AvatarSelector } from './AvatarSelector';

export function ProfilePhotoUpload({ className = '' }: { className?: string }) {
  const { profile, updateProfile } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file.');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert('File is too large (max 5MB).');
      return;
    }

    setUploading(true);
    
    try {
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64String = reader.result as string;
        
        const res = await fetch('/api/auth/update-profile-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId: profile?._id, imageBase64: base64String })
        });
        
        const data = await res.json();
        if (res.ok) {
          updateProfile({ profileImage: data.url });
          setShowModal(false);
        } else {
          alert('Failed to upload image: ' + data.error);
        }
        setUploading(false);
      };
      reader.readAsDataURL(file);
    } catch (err) {
      console.error('Error uploading photo', err);
      alert('Error uploading photo');
      setUploading(false);
    }
  };

  const handleSelectAvatar = async (url: string) => {
    try {
      const res = await fetch('/api/auth/update-avatar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: profile?._id, avatarUrl: url })
      });
      if (res.ok) {
        updateProfile({ avatarUrl: url, profileImage: undefined });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const getInitials = () => {
    if (!profile?.displayName) return '?';
    return profile.displayName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  const currentImage = profile?.profileImage || profile?.avatarUrl;

  return (
    <>
      <div className={`relative group cursor-pointer ${className || "w-10 h-10"}`} onClick={() => setShowModal(true)}>
        <div className="w-full h-full rounded-full overflow-hidden bg-gray-200 dark:bg-gray-800 border-2 border-white/20 flex items-center justify-center text-gray-700 dark:text-gray-300 font-bold shadow-sm relative">
          {currentImage ? (
            <img src={currentImage} alt="Profile" className="w-full h-full object-cover" />
          ) : (
            <span>{getInitials()}</span>
          )}
          
          <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            {uploading ? (
              <Loader2 size={16} className="text-white animate-spin" />
            ) : (
              <Camera size={16} className="text-white" />
            )}
          </div>
        </div>
      </div>
      
      {showModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl w-full max-w-md relative">
            <button onClick={() => setShowModal(false)} className="absolute top-4 right-4 text-gray-500 hover:text-gray-900 dark:text-white transition-colors">
              <X size={24} />
            </button>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">Customize Profile Photo</h3>
            
            <AvatarSelector value={profile?.avatarUrl || ''} onChange={handleSelectAvatar} />
            
            <div className="mt-8 pt-6 border-t border-gray-200 dark:border-white/10 flex flex-col gap-3">
               <label className="text-sm font-bold text-gray-700 dark:text-gray-300">Or Upload Custom Photo</label>
               <button onClick={() => fileInputRef.current?.click()} className="flex items-center justify-center gap-2 w-full py-3 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 rounded-xl transition-colors font-semibold text-gray-900 dark:text-white">
                 <Upload size={18} /> Choose File
               </button>
            </div>
          </div>
        </div>
      )}
      
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        accept="image/*" 
        className="hidden" 
      />
    </>
  );
}
