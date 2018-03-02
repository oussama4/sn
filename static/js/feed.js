new Vue({
  el: '#post',
  data: {
    post_text: '',
    selectedImage: null
  },
  methods: {
    onFileChanged (event) {
      this.selectedImage = event.target.files[0]
    },
    onUpload () {
      var csrftoken = Cookies.get('csrftoken')
      var formData = new FormData()
      formData.append('post_text', this.post_text)
      formData.append('post_image', this.selectedImage)

      fetch('/feed/post', {
        method: 'POST',
        headers: {
          'content-type': 'multipart/form-data',
          'X-CSRFToken': csrftoken
        },
        body: formData
      })
    }
  }
})
