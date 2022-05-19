fetch("http://127.0.0.1:5000/upload", options)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.log(error);
  });


  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  const options = {
    method: "POST",
    body: formData,
  };
  