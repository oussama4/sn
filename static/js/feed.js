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
    limit: 10,
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
        targetActor{
          id
          firstName
          lastName
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
      console.log(res.data)
      this.actions = res.data.data.actions
    }).catch(err => console.log(err))
  },
  methods: {
    fetchActions: function () {
      this.offset += 10
      this.limit += 10
      var query = `
      query getActions{
        actions(limit:${this.limit}, offset:${this.offset}){
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
          targetActor{
            id
            firstName
            lastName
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
        console.log(res.data)
        this.actions = this.actions.concat(res.data.data.actions)
      }).catch(err => console.log(err))
    },
    onLike (action) {
      this.createAction(action, 'like')
    },
    onShare (action) {
      this.createAction(action, 'share')
    },
    createAction (action, verb) {
      var query = `
      mutation actCreate($input:ActionInput){
        createAction(action:$input){
          id
          verb
        }
      }
      `
      var csrftoken = Cookies.get('csrftoken')
      axios.post('graphql/', JSON.stringify({
        query: query,
        variables: {
          input: {
            verb: verb,
            post: action.target.id,
            targetActor: action.actor.id
          }
        }
      }), {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
          'content-type': 'application/json'
        }
      }).then(res => {
        console.log(res.data)
      }).catch(err => console.log(err))
    }
  },
  filters: {
    ago: function (value) {
      var timeagoInstance = timeago()
      return timeagoInstance.format(value)
    }
  },
  mounted () {
    var vueInstance = this
    window.addEventListener('scroll', function (e) {
      var scrollTop = $(document).scrollTop()
      var bodyheight = $(document).height() - $(window).height()
      var block_request = false
      var empty_response = false;   
      // todo : empty response   
      if (scrollTop / bodyheight > 0.9 && !block_request && !empty_response) {
        block_request = true
        console.log('beforefetch')
        vueInstance.fetchActions()
        console.log('fetched')
        block_request = false
      }
    })
  }
})
