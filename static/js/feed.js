var postInput = new Vue({
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

var feed = new Vue({
  delimiters: ["[[", "]]"],
  el: '#feed',
  data: {
    offset: 0,
    actions: []
  },
  created () {
    var query = `
    query getActions{
      actions(limit:10, offset:0){
        id
        verb
        created
        actor{
          id
          email
          firstName
          lastName
          avatar
        }
        target{
          id
          text
          image
        }
      }
    }
    `
    var csrftoken = Cookies.get('csrftoken')
    axios.post('graphql/', JSON.stringify({query: query}), {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrftoken,
        'content-type': 'application/json'
      }
    }).then(res => {
      this.actions = res.data.data.actions
    }).catch(err => console.log(err))
  }
})
