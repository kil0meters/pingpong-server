<template>
  <div id="app">
  <div class="container-fluid h-100">
    <div class="row h-100">
      <div class="col-md-3 main-column">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <a class="navbar-brand" href="#">PingPong Web</a>
        </nav>
        <nav class="d-none d-md-block bg-light sidebar h-100">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link" v-bind:class="{'nav-link-focus': currentPage === 'remote'}" href="#" @click="currentPage = 'remote'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-wifi"><path d="M5 12.55a11 11 0 0 1 14.08 0"></path><path d="M1.42 9a16 16 0 0 1 21.16 0"></path><path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path><line x1="12" y1="20" x2="12.01" y2="20"></line></svg>
                  Remote
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" v-bind:class="{'nav-link-focus': currentPage === 'drills'}" href="#" @click="currentPage = 'drills'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bookmark"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                  Drills
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" v-bind:class="{'nav-link-focus': currentPage === 'authorized_devices'}" href="#" @click="currentPage = 'authorized_devices'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-key"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"></path></svg>
                  Authorized Devices
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" v-bind:class="{'nav-link-focus': currentPage === 'logs'}" href="#" @click="currentPage = 'logs'">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-settings"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                  Logs
                </a>
              </li>
            </ul>
          </div>
        </nav>
      </div>
      <div class="col-md-9 main-column">
        <main class="conatainer" role="main">
          <div v-if="currentPage === 'remote'">
            <RemotePage />
          </div>
          <div v-else-if="currentPage === 'drills'">
            <DrillsPage />
          </div>
          <div v-else-if="currentPage === 'authorized_devices'">
            <AuthorizedDevicesPage />
          </div>
          <div v-else-if="currentPage === 'logs'">
            <LogsPage />
          </div>
        </main>
        <footer class="footer">
          <div class="container">
            <span class="text-muted">Created with 🏓 by <a href="https://twitter.com/kil0meters">kilometers</a></span>
          </div>
        </footer>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import RemotePage from './components/RemotePage.vue'
import DrillsPage from './components/DrillsPage.vue'
import AuthorizedDevicesPage from './components/AuthorizedDevicesPage.vue'
import LogsPage from './components/LogsPage.vue'

export default {
  name: 'app',
  components: {RemotePage, DrillsPage, AuthorizedDevicesPage, LogsPage},
  data () {
    return {
      currentPage: 'remote',
    }
  }
}
</script>

<style>

html, body, #app {
  height: 100% !important;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

/* .row {
  margin-right: auto !important; /* required or overflow happens for some reason 
} */

.main-column {
  padding: 0;
}

.navbar {
  background-color: #007bff !important;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
  height: 64px;
}

.nav-link-focus {
  font-weight: bold;
  color: #0056b3;
}


.sidebar-sticky {
  height: 100% !important;
  margin-top: -64px;
  padding-top: 64px;
}

.navbar-brand {
  padding: 0 15px;
}

.sidebar {
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 60px;
  line-height: 60px;
  background-color: #f5f5f5;
  box-shadow: inset 0 1px 0 rgba(0, 0, 0, .1);
}

.footer .container {
  margin: 0;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
