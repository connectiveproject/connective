<template>
  <div class="note">
    <p class="text-center">
      <slot></slot>
    </p>
  </div>
</template>

<style scoped lang="scss">
.note {
  position: relative;
  width: 300px;
  min-height: 100px;
  margin: 25px auto;
  padding: 45px 15px 15px 15px;
  background-color: #fff400;
  -webkit-box-shadow: 0 2px 12px rgba(0, 0, 0, 0.7);
  -moz-box-shadow: 0 2px 12px rgba(0, 0, 0, 0.7);
  box-shadow: 0 1px 2px #000;
  //  background: #fff url(https://our.fogbugz.com/images/tbKiwiLogo.gif) no-repeat
  //   4px 8px;
}

.note p {
  font-size: 36px;
  overflow: hidden;
}

.note::before {
  content: " ";
  display: block;
  position: absolute;
  left: 115px;
  top: -15px;
  width: 75px;
  height: 25px;
  z-index: 2;
  background-color: rgba(243, 245, 228, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.5);
  -webkit-box-shadow: 0 0 5px #888;
  -moz-box-shadow: 0 0 5px #888;
  box-shadow: 2px 2px 2px #000;
  -webkit-transform: rotate(6deg);
  -moz-transform: rotate(6deg);
  -o-transform: rotate(6deg);
}
</style>
