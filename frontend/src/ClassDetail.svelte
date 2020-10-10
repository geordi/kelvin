<script>
  import {push, link} from 'svelte-spa-router'
  import {fetch} from './api.js'
  import CopyToClipboard from './CopyToClipboard.svelte'

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let clazz;

  let addStudentError = [];
  let showAddStudents = false;
  async function addStudent(form, class_id) {
    addStudentError = [];
    const textarea = form.querySelector('textarea');
    const logins = textarea
        .value
        .split('\n')
        .map(login => login.replace(/^\s+|\s+$/g, ''))
        .filter(login => login.length);

    if(!logins.length) {
      return;
    }

    try {
      let req = await fetch(`/api/classes/${class_id}/add_students`, {
        method: 'POST',
        body: JSON.stringify({'username': logins})
      });
      let res = await req.json();
      if(res) {
        if(res['not_found'].length) {
          addStudentError = 'Not found users left in textarea.';
          textarea.value = res['not_found'].join('\n');
          dispatch('update');
        } else if(res['success'] === true) {
          textarea.value = '';
          dispatch('update');
        } else {
          addStudentError = res['error'] || 'Unknown error';
        } 
      }
    } catch(err) {
      addStudentError = 'Error: ' + err;
    }
  }
</script>

<style>
td, th {
  white-space: nowrap;
  width: 1%;
}
tr th:last-of-type {
  width: 100%;
}
tr td:not(:nth-of-type(1)):not(:nth-of-type(2)) {
  text-align: center;
}
</style>

<div class="card mb-2" style="position: initial">
  <div class="card-header p-0">
      <div class="float-right p-2">
        <span style="cursor: pointer" on:click={() => showAddStudents = !showAddStudents}>
          <span class="iconify" data-icon="ant-design:user-add-outlined"></span>
        </span>
        <a href="/task/add/{clazz.subject_abbr}" use:link title="Assign new task" style="color: black">
          <span class="iconify" data-icon="bx:bx-calendar-plus"></span>
        </a>
        <a href="{clazz.csv_link}" title="Download CSV with results for all task" style="color: black">
          <span class="iconify" data-icon="la:file-csv-solid"></span>
        </a>
      </div>
      <button class="btn">
          {clazz.subject_abbr} {clazz.timeslot} {clazz.code} {clazz.teacher_username}
          <span class="text-muted">({clazz.students.length} students)</span>
      </button>
  </div>
  <div> 
    <div class="card-body">
      {#if showAddStudents}
      <form class="col-sm-3 p-0 mb-2" on:submit|preventDefault={(e) => addStudent(e.target.closest('form'), clazz.id)}>
        <div class="input-group input-group-sm">
          <textarea class="form-control" placeholder="Add student logins to this class"></textarea>
          <div class="input-group-append">
            <button class="btn btn-primary">+</button>
          </div>
        </div>
      </form>
      {#if addStudentError}
        <span class="text-danger">{addStudentError}</span>
      {/if}
      {/if}

      {@html clazz.summary}
      <table class="table table-sm table-hover">
        <thead>
          <tr>
            <th>
              Login<!--
              --><CopyToClipboard content={clazz.students.map(s => s.username).join('\n')} title='Copy logins to clipboard'>
                <span class="iconify" data-icon="clarity:clipboard-line"></span>
              </CopyToClipboard><!--
              --><CopyToClipboard content={clazz.students.map(s => s.username + '@vsb.cz').join('\n')} title='Copy emails to clipboard'>
                <span class="iconify" data-icon="ic:round-alternate-email"></span>
              </CopyToClipboard>
            </th>
            <th>Student</th>
            {#each clazz.assignments as assignment}
            <th class="more-hover">
              <a href="{ assignment.task_link }">{ assignment.short_name }</a>
              <div class="more-content">
                {assignment.name}
                <a href="/task/edit/{assignment.task_id}" use:link class="text-muted" title="Edit"><i class="fas fa-pen"></i></a>
                <div>
                  <a href="{assignment.moss_link}" title="Send to MOSS"><i class="fas fa-check-double"></i></a>
                  <a href="{assignment.sources_link}" title="Download all source codes"><i class="fas fa-download"></i></a>
                  <a href="{assignment.csv_link}" title="Download CSV with results"><i class="fas fa-file-csv"></i></a>
                </div>
                <dl>
                  <dt>Assigned</dt>
                  <dd>
                    {assignment.assigned}
                  </dd>

                  <dt>Deadline</dt>
                  <dd>
                    {assignment.deadline}
                  </dd>

                  {#if assignment.max_points}
                  <dt>Max points</dt>
                  <dd>
                    {assignment.max_points} 
                  </dd>
                  {/if}
                </dl>
              </div>
            </th>
            {/each}
            <th></th>
          </tr>
        </thead>

        <tbody>
        {#each clazz.students as student}
        <tr>
          <td>{ student.username }</td>
          <td>{ student.last_name } { student.first_name }</td>
          {#each clazz.assignments.map(i => i.students[student.username]) as result}
            <td>
              {#if result.submits != 0}
                <a href={result.link} style="color: {result.color}">
                  { isNaN(parseFloat(result.assigned_points)) ? '?' : result.assigned_points}
                </a>
              {/if}
            </td>
          {/each}
          <td></td>
        </tr>
        {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>