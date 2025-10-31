const form = document.getElementById('uploadForm');
const dropzone = document.getElementById('dropzone');
const imageInput = document.getElementById('imageInput');
const result = document.getElementById('result');
const origImg = document.getElementById('origImg');
const procImg = document.getElementById('procImg');
const downloadBtn = document.getElementById('downloadBtn');

// Show preview when file chosen
imageInput.addEventListener('change', e => {
  const f = e.target.files[0];
  if(!f) return;
  origImg.src = URL.createObjectURL(f);
  result.hidden = false;
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const btn = form.querySelector('button');
  btn.disabled = true; btn.textContent = 'Processing...';

  try {
    const res = await fetch('/upload', {method:'POST', body:fd});
    if(!res.ok) throw new Error('Server error');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    procImg.src = url;
    downloadBtn.href = url;
    result.hidden = false;
  } catch(err){
    alert('Upload failed: '+err.message);
  } finally{
    btn.disabled = false; btn.textContent='Upload & Remove Background';
  }
});

['dragenter','dragover','dragleave','drop'].forEach(ev => {
  dropzone.addEventListener(ev, (e)=>{e.preventDefault();e.stopPropagation();});
});

dropzone.addEventListener('drop', e => {
  const f = e.dataTransfer.files[0];
  if(!f) return;
  imageInput.files = e.dataTransfer.files;
  origImg.src = URL.createObjectURL(f);
  result.hidden = false;
});