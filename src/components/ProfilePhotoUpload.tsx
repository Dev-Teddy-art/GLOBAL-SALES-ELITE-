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
        await updateProfile({ profileImage: base64String, avatarUrl: base64String });
        setUploading(false);
        setShowModal(false);
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
      await updateProfile({ avatarUrl: url, profileImage: url });
      setShowModal(false);
    } catch (e) {
      console.error('Failed to set avatar', e);
    }
  };

  const getInitials = () => {
    const name = profile?.name || profile?.displayName || (profile?.firstName ? `${profile.firstName} ${profile.lastName || ''}` : '');
    if (!name.trim()) return '?';
    return name.trim().split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  };

  const currentImage = profile?.profileImage || profile?.avatarUrl;

  return (
    <>
      <div className={`relative group cursor-pointer ${className || "w-10 h-10"}`} onClick={() => setShowModal(true)}>
        <div className="w-full h-full rounded-full overflow-hidden bg-slate-800 border-2 border-white/20 flex items-center justify-center text-white font-bold shadow-sm relative">
          {currentImage ? (
            <img src={currentImage} alt="Profile" className="w-full h-full object-cover" />
          ) : (
            <span>{getInitials()}</span>
          )}

          <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-full">
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
          <div className="bg-slate-900 border border-slate-700 rounded-3xl p-6 shadow-2xl w-full max-w-md relative text-white">
            <button onClick={() => setShowModal(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors">
              <X size={24} />
            </button>
            <h3 className="text-xl font-bold mb-6">Customize Profile Photo</h3>

            <AvatarSelector value={profile?.avatarUrl || ''} onChange={handleSelectAvatar} />

            <div className="mt-8 pt-6 border-t border-slate-800 flex flex-col gap-3">
              <label className="text-sm font-bold text-slate-300">Or Upload Custom Photo</label>
              <button onClick={() => fileInputRef.current?.click()} className="flex items-center justify-center gap-2 w-full py-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors font-semibold text-white">
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
