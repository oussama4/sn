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
      console.log('iamge:', this.selectedImage)

      axios.post('/feed/post', formData, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
          'content-type': 'multipart/form-data'
        }
      }).then(res => console.log(res)).catch(err => console.log(err))
    }
  }
})
