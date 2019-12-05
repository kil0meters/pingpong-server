<template>
  <div class="card">
    <div class="card-body">
      <h2>Remote</h2>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          Current firing speed is {{ firing_speed }}
          <input v-model="firing_speed" type="range" class="custom-range" min="5" max="70"></input>
        </li>
        <li class="list-group-item">
          Current oscillation frequency is {{ oscillation_frequency }}
          <input v-model="oscillation_frequency" type="range" class="custom-range" min="0" max="100"></input>
        </li>
        <li class="list-group-item">
          Current topspin is {{ topspin }}
          <input v-model="topspin" type="range" class="custom-range" min="0" max="100"></input>
        </li>
        <li class="list-group-item">
          Current backspin {{ backspin }}
          <input v-model="backspin" type="range" class="custom-range" min="0" max="100"></input>
        </li>
      </ul>
      <button type="button" class="btn btn-primary">Update drill</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "RemotePage",
  data () {
    return {
      firing_speed: 0,
      oscillation_frequency: 0,
      topspin: 0,
      backspin: 0,
    }
  }
}
</script>

<style scoped>
.card {
  margin: 16px;
  padding: 12px;
}
</style>