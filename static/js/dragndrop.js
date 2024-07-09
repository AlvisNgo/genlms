(function () {

  'use strict';
  
    const preventDefaults = event => {
    event.preventDefault();
    event.stopPropagation();
    };

    // Highlight styles
    const highlight = event =>
        event.target.classList.add('highlight');
    const unhighlight = event =>
        event.target.classList.remove('highlight');

    const getInputAndGalleryRefs = element => {
        const zone = element.closest('.upload_dropZone') || false;
        const gallery = zone.querySelector('.upload_gallery') || false;
        const input = zone.querySelector('input[type="file"]') || false;
        return {input: input, gallery: gallery};
    }

    const handleDrop = event => {
        const dataRefs = getInputAndGalleryRefs(event.target);
        dataRefs.files = event.dataTransfer.files;
        handleFiles(dataRefs);
    }

    const eventHandlers = zone => {
        const dataRefs = getInputAndGalleryRefs(zone);
        if (!dataRefs.input) return;

        // Prevent default drag behaviors
        ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
        zone.addEventListener(event, preventDefaults, false);
        document.body.addEventListener(event, preventDefaults, false);
        });

        // Highlighting drop area when item is dragged over it
        ;['dragenter', 'dragover'].forEach(event => {
        zone.addEventListener(event, highlight, false);
        });
        ;['dragleave', 'drop'].forEach(event => {
        zone.addEventListener(event, unhighlight, false);
        });

        // Handle dropped files
        zone.addEventListener('drop', handleDrop, false);

        // Handle browse selected files
        dataRefs.input.addEventListener('change', event => {
        dataRefs.files = event.target.files;
        handleFiles(dataRefs);
        }, false);
    }

    // Initialise Dropzones
    const dropZones = document.querySelectorAll('.upload_dropZone');
    for (const zone of dropZones) {
        eventHandlers(zone);
    }

    // Perform secondary upload checking (console log ppt and word to determine filetype)
    const isFile = file => 
        ['image/jpeg', 'image/png', 'application/pdf','application/msword','application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',].includes(file.type);

    function previewFiles(dataRefs) {
      if (!dataRefs.gallery) {
          return;
      }
        // Iterate uploaded file
      for (const file of dataRefs.files) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
          let element;
          // PDF & MS Files (Change to iframe if you want a pdf preview)
          if (file.type.startsWith('application/')){
              element = document.createElement('div');
              element.className = 'upload_file';
              element.textContent = `File: ${file.name}`;
          } 
          // Image Files (Change to img if you want an image preview)
          if (file.type.startsWith('image/')){
              element = document.createElement('div');
              element.className = 'upload_file';
              element.setAttribute('alt', file.name);
              element.textContent = `File: ${file.name}`;
          }
          let input = document.querySelector('input[type="file"]');
          console.log(input)

          // Add file to wrapper
          const wrapper = document.createElement('div');
          wrapper.className = 'file-wrapper';
          element.src = reader.result;
          dataRefs.gallery.appendChild(element);
          input.appendChild(element)
          wrapper.appendChild(element);

          // Add delete button foreach file to wrapper
          const deleteButton = document.createElement('button');
          deleteButton.textContent = 'Remove';
          deleteButton.className = 'btn btn-danger delete-btn';
          deleteButton.onclick = function() {
              dataRefs.gallery.removeChild(wrapper);
              dataRefs.files = Array.from(dataRefs.files).filter(f => f !== file);
          };
          wrapper.appendChild(deleteButton);  
          dataRefs.gallery.appendChild(wrapper);
          console.log(dataRefs);

        }
      }
    }

  // const fileUpload = dataRefs => {
  //   const formData = new FormData();
  //   formData.append(name, dataRefs.files);
  //   console.log(dataRefs.files)

  //   fetch(url, {
  //     method: 'POST',
  //     body: formData
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log('posted: ', data);
  //     if (data.success === true) {
  //       previewFiles(dataRefs);
  //     } else {
  //       console.log('URL: ', url, '  name: ', name)
  //     }
  //   })
  //   .catch(error => {
  //     console.error('errored: ', error);
  //   });
  // }


  // Handle both selected and dropped files
  const handleFiles = dataRefs => {

    let files = [...dataRefs.files];

    // Remove unaccepted file types
    files = files.filter(item => {
      if (!isFile(item)) {
        console.log('File type not supported, ', item.type);
      }
      return isFile(item) ? item : null;
    });

    if (!files.length) return;
    dataRefs.files = files;

    previewFiles(dataRefs);
    // fileUpload(dataRefs);
  }

})();